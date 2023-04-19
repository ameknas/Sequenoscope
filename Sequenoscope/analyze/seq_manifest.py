#!/usr/bin/env python

from Sequenoscope.utils.parser import fastq_parser
from Sequenoscope.analyze.bam import BamProcessor
from Sequenoscope.utils.__init__ import is_non_zero_file
import os
from math import log

class SeqManifest:
    fields = [
        'sample_id','read_id','read_len','read_qscore','channel',
        'start_time','end_time','decision','fastp_status',
        'is_mapped','is_uniq','contig_id',
    ]
    sample_id = ''
    in_seq_summary = ''
    read_list = ''
    out_prefix = ''
    out_dir = ''
    bam_obj = None
    fastp_obj = None
    fastp_fastq = []
    delim = "\t"
    status = False
    error_msg = ''
    start_time = ''
    end_time = ''
    filtered_reads = {}
    error_messages = None

    def __init__(self,sample_id,in_bam,out_prefix, out_dir,fastp_fastq=None,in_seq_summary=None, read_list=None,start_time=None,end_time=None,delim="\t"):
        """
        Initalize the class with sample_id, in_bam, out_prefix, and out_dir. Analyze reads based on seq summary and 
        fastp fast availbility by producing manifest files.

        Arguments:
            sample_id: str
                a string of the name of the sample to be analyzed
            in_bam: str
                a string to the path where the bam file is stored
            out_prefix: str
                a designation of what the output files will be named
            out_dir: str
                a designation of the output directory
            fastq_fastq: str
                a designation of where the filitered fastq produced by fastp is stored.
            in_seq_summary: str
                a designation of where the sequencing summary produced by the Nanopore sequencers is stored
            read_list: str
                a designation of where the read list produced from the original fastq is stored
            start_time: int
                an integer representing the start time when seq summary isn't provided.
            end_time: int
                an integer representing the end time when seq summary isn't provided.
            delim: str
                a string that designates the delimiter used to parse files. default is tab delimiter
        """
        self.delim = delim
        self.out_prefix = out_prefix
        self.out_dir = out_dir
        self.sample_id = sample_id
        self.in_seq_summary = in_seq_summary
        self.fastp_fastq = fastp_fastq
        self.start_time = start_time
        self.end_time = end_time
        self.read_list = read_list

        if self.in_seq_summary is None:
            if start_time is None or end_time is None:
                self.status = False
                self.error_msg = 'Error no sequence summary specified, please specify a start and end datetime'
                return

        self.bam_obj = BamProcessor(input_file=in_bam)
        if self.fastp_fastq is not None:
            self.process_fastq(self.fastp_fastq)

        if self.in_seq_summary is not None and not is_non_zero_file(self.in_seq_summary):
            self.status = False
            self.error_msg = "Error specified seq summary file {} does not exist".format(self.in_seq_summary)
            return
        if self.in_seq_summary is not None:
            self.create_manifest_with_sum()
        else:
            self.create_manifest_no_sum()
    
    def error_prob_list_tab(n):
        """
        generate a list of error rates for qualities less than or equal to n.
        source: github.com/wdecoster/nanoget/blob/master/nanoget/utils.py

        Arguments: 
            n: error probability threshold

        Returns:
            list:
                list of error rates
        """
        return [10**(q / -10) for q in range(n+1)]

    def calc_mean_qscores(self,qual,tab=error_prob_list_tab(128)):
        """
        Calculates the mean quality score for a read where they have been converted to Phred.
        Phred scores are first converted to probabilites, then the average error probability is calculated.
        The average is then converted back to the Phred scale.

        Arguments:
            qual: string
                string of Phred 33 ints for quality calcualtions
            
            tab: list
                list of error rates for qaulties specified

        Returns:
            float:
                mean qscore
        """
        if qual:
            phred_score = -10 * log(sum([tab[q] for q in qual]) / len(qual) , 10)
            return phred_score
        else:
            return 0

    def convert_qscores(self,qual_string):
        """
        Calculates the mean quality score for a read where they have been converted to Phred

        Arguments
            qual_string: string of phred 33 ints for quality

        Returns:
            float:
                mean qscore
        """
        qual_values = []
        for c in qual_string:
            qual_values.append(ord(c) - 33)

        return qual_values

    def process_fastq(self,fastq_file_list):
        """
        Process the fastq file and extract reads, quality, and qscores

        Argument:
            fastq_file_list:
                list of fastq files
        """
        for fastq_file in fastq_file_list:
            fastq_obj = fastq_parser(fastq_file)
            for record in fastq_obj.parse():
                read_id = fastq_obj.read_id_from_record
                seq = record[1]
                seq_len = len(seq)
                qual = self.convert_qscores(record[3])
                qscore = self.calc_mean_qscores(qual)
                self.filtered_reads[read_id] = [seq_len,qscore]

    def create_row(self):
        """
        create rows and store them into a dictionary

        Returns:
            dict:
                dictionary of rows produced.
        """
        out_row = {}
        for field_id in self.fields:
            out_row[field_id] = ''
        return out_row

    def create_manifest_with_sum(self):
        """
        Create a manifest file with various statistics when a sequencing summary is present

        Returns: 
            file object: 
                seq manifest text file
        """
        manifest_file = os.path.join(self.out_dir,"{}.txt".format(self.out_prefix))
        fout = open(manifest_file,'w')
        fout.write("{}\n".format("\t".join(self.fields)))

        fin = open(self.in_seq_summary,'r')
        header = next(fin).strip().split(self.delim)

        for line in fin:
            row = line.strip().split(self.delim)
            row_data = {}
            for i in range(0,len(row)) :
                row_data[header[i]] = row[i]

            read_id = row_data['read_id']
            #read_len = 0
            #read_qual = 0
            read_len = row_data['sequence_length_template']
            read_qual = row_data['mean_qscore_template']
            is_uniq = True
            is_mapped = False
            start_time = row_data['start_time']
            end_time = ''
            duration = row_data['duration']
            if start_time == '':
                start_time = self.start_time
                end_time = self.end_time
            else:
                start_time = float(start_time)
                if duration != '':
                    end_time = start_time + float(duration)

            out_row = self.create_row()
            for field_id in self.fields:
                if field_id in row_data:
                    out_row[field_id] = row_data[field_id]
            mapped_contigs = []
            for contig_id in self.bam_obj.ref_stats:
                if read_id in self.bam_obj.ref_stats[contig_id]['reads']:
                    #read_len = self.bam_obj.ref_stats[contig_id]['reads'][read_id][0]
                    #read_qual = self.bam_obj.ref_stats[contig_id]['reads'][read_id][1]
                    pass
                    if contig_id != '*':
                        mapped_contigs.append(contig_id)

            if len(mapped_contigs) > 0:
                is_mapped = True
            if len(mapped_contigs) > 1:
                is_uniq = False

            fastp_status = False
            if read_id in self.filtered_reads:
                fastp_status = True
            out_row['fastp_status'] = fastp_status
            out_row['sample_id'] = self.sample_id
            out_row['read_id'] = read_id
            out_row['is_mapped'] = is_mapped
            out_row['is_uniq'] = is_uniq
            out_row['read_len'] = read_len
            out_row['read_qscore'] = read_qual
            out_row['start_time'] = start_time
            out_row['end_time'] = end_time
            out_row['decision'] = row_data['end_reason']


            if len(mapped_contigs) == 0:
                out_row['contig_id'] = ''
                fout.write("{}\n".format("\t".join([str(x) for x in out_row.values()])))

            for contig_id in mapped_contigs:
                out_row['contig_id'] = contig_id
                fout.write("{}\n".format("\t".join([str(x) for x in out_row.values()])))

        self.status = self.check_files([manifest_file])
        if self.status == False:
            self.error_messages = "one or more files was not created or was empty"
            raise ValueError(str(self.error_messages))
        
        fin.close()
        fout.close()

    def create_manifest_no_sum(self):
        """
        Create a manifest file with various statistics when a sequencing summary is NOT present. Uses read list 
        file instead.

        Returns: 
            file object: 
                seq manifest text file
        """
        
        manifest_file = os.path.join(self.out_dir,"{}.txt".format(self.out_prefix))
        fout = open(manifest_file,'w')
        fout.write("{}\n".format("\t".join(self.fields)))

        fin = open(self.read_list,'r')
        header = next(fin).strip().split(self.delim)

        for line in fin:
            row = line.strip().split(self.delim)
            row_data = {}
            for i in range(0,len(row)) :
                row_data[header[i]] = row[i]

            read_id = row_data['read_id']
            read_len = 0
            read_qual = 0
            is_uniq = True
            is_mapped = False
            start_time = self.start_time
            end_time = self.end_time

            out_row = self.create_row()
            for field_id in self.fields:
                if field_id in row_data:
                    out_row[field_id] = row_data[field_id]
            mapped_contigs = []
            for contig_id in self.bam_obj.ref_stats:
                if read_id in self.bam_obj.ref_stats[contig_id]['reads']:
                    read_len = self.bam_obj.ref_stats[contig_id]['reads'][read_id][0]
                    read_qual = self.bam_obj.ref_stats[contig_id]['reads'][read_id][1]
                    if contig_id != '*':
                        mapped_contigs.append(contig_id)

            if len(mapped_contigs) > 0:
                is_mapped = True
            if len(mapped_contigs) > 1:
                is_uniq = False

            fastp_status = False
            if read_id in self.filtered_reads:
                fastp_status = True
            out_row['fastp_status'] = fastp_status
            out_row['sample_id'] = self.sample_id
            out_row['read_id'] = read_id
            out_row['is_mapped'] = is_mapped
            out_row['is_uniq'] = is_uniq
            out_row['read_len'] = read_len
            out_row['read_qscore'] = read_qual
            out_row['start_time'] = start_time
            out_row['end_time'] = end_time
            out_row['decision'] = "N/A"
            out_row['channel'] = "N/A"


            if len(mapped_contigs) == 0:
                out_row['contig_id'] = ''
                fout.write("{}\n".format("\t".join([str(x) for x in out_row.values()])))

            for contig_id in mapped_contigs:
                out_row['contig_id'] = contig_id
                fout.write("{}\n".format("\t".join([str(x) for x in out_row.values()])))

        self.status = self.check_files([manifest_file])
        if self.status == False:
            self.error_messages = "one or more files was not created or was empty"
            raise ValueError(str(self.error_messages))
        
        fin.close()
        fout.close()

    def check_files(self, files_to_check):
        """
        check if the output file exists and is not empty

        Arguments:
            files_to_check: list
                list of file paths

        Returns:
            bool:
                returns True if the generated output file is found and not empty, False otherwise
        """
        if isinstance (files_to_check, str):
            files_to_check = [files_to_check]
        for f in files_to_check:
            if not os.path.isfile(f):
                return False
            elif os.path.getsize(f) == 0:
                return False
        return True