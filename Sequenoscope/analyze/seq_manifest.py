#!/usr/bin/env python

from Sequenoscope.utils.parser import fastq_parser
from Sequenoscope.analyze.bam import BamProcessor
from Sequenoscope.utils.__init__ import is_non_zero_file

class SeqManifest:
    fields = [
        'sample_id','read_id','read_len','read_qscore','channel',
        'start_time','end_time','decision','fastp_status',
        'is_mapped','is_uniq','contig_id',
    ]
    sample_id = ''
    in_seq_summary = ''
    out_file = ''
    bam_obj = None
    fastp_obj = None
    delim = "\t"
    status = True
    error_msg = ''
    start_time = ''
    end_time = ''
    #filtered_reads = set()
    filtered_reads = dict()

    def __init__(self,sample_id,in_bam,out_file,fastp_fastq=None,in_seq_summary=None,start_time=None,end_time=None,delim="\t"):
        self.delim = delim
        self.out_file = out_file
        self.sample_id = sample_id
        self.in_seq_summary = in_seq_summary
        self.fastp_fastq = fastp_fastq

        if self.in_seq_summary is None:
            if start_time is None or end_time is None:
                self.status = False
                self.error_msg = 'Error no sequence summary specified, please specify as start and end datetime'
                return

        self.bam_obj = BamProcessor(input_file=in_bam)
        if self.fastp_fastq is not None:
            self.process_fastq(self.fastp_fastq)

        if self.in_seq_summary is not None and not is_non_zero_file(self.in_seq_summary):
            self.status = False
            self.error_msg = "Error specified seq summary file {} does not exist".format(self.in_seq_summary)
            return
        if self.in_seq_summary is not None:
            self.create_nanopore_manifest()
        else:
            self.create_illumina_manifest()

    def calc_mean_qscores(self,qual):
        '''
        Calculates the mean quality score for a read where they have been converted to phred
        :param qual: string of phred 33 ints for quality
        :return: float mean qscore
        '''
        score = sum(qual)
        length = len(qual)
        if length == 0:
            return 0

        return score / length

    def convert_qscores(self,qual_string):
        '''
        Calculates the mean quality score for a read where they have been converted to phred
        :param qual: string of phred 33 ints for quality
        :return: float mean qscore
        '''
        qual_values = []
        for c in qual_string:
            qual_values.append(ord(c) - 33)

        return qual_values

    def process_fastq(self,fastq_file):
        fastq_obj = fastq_parser(fastq_file)
        for record in fastq_obj.parse():
            read_id = record[0][1:]
            seq = record[1]
            seq_len = len(seq)
            qual = self.convert_qscores(record[3])
            qscore = self.calc_mean_qscores(qual)
            self.filtered_reads[read_id] = [seq_len,qscore]



    def create_row(self):
        out_row = {}
        for field_id in self.fields:
            out_row[field_id] = ''
        return out_row

    def create_nanopore_manifest(self):
        '''

        :return:
        '''
        fout = open(self.out_file,'w')
        fout.write("{}".format("\t".join(self.fields)))

        fin = open(self.in_seq_summary,'r')
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
            start_time = row['start_time']
            end_time = ''
            duration = row['duration']
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
            out_row['read_qual'] = read_qual
            out_row['start_time'] = start_time
            out_row['end_time'] = end_time
            out_row['decision'] = row_data['end_reason']


            if len(mapped_contigs) == 0:
                out_row['contig_id'] = ''
                fout.write("{}".format("\t".join([str(x) for x in out_row.values()])))

            for contig_id in mapped_contigs:
                out_row['contig_id'] = contig_id
                fout.write("{}".format("\t".join([str(x) for x in out_row.values()])))

        fin.close()
        fout.close()

    def create_illumina_manifest(self):
        '''

        :return:
        '''
        fout = open(self.out_file, 'w')
        fout.write("{}".format("\t".join(self.fields)))

        for contig_id in self.bam_obj:
            for read_id in self.bam_obj[contig_id]['reads']:
                out_row = self.create_row()
                is_mapped = False
                mapped_contigs = []
                for cid in self.bam_obj:
                    if cid == '*':
                        continue
                    if read_id in self.bam_obj[cid]['reads']:
                        mapped_contigs.append(cid)
                is_uniq = False
                if len(mapped_contigs) == 1:
                    is_uniq = True
                if len(mapped_contigs) > 0:
                    is_mapped = True
                    cid = ''
                else:
                    cid = contig_id

                fastp_status = False
                if read_id in self.filtered_reads:
                    fastp_status = True

                read_len = self.bam_obj[contig_id]['reads'][read_id][0]
                read_qual = self.bam_obj[contig_id]['reads'][read_id][0]
                out_row['sample_id'] = self.sample_id
                out_row['fastp_status'] = fastp_status
                out_row['read_id'] = read_id
                out_row['is_mapped'] = is_mapped
                out_row['is_uniq'] = is_uniq
                out_row['read_len'] = read_len
                out_row['read_qual'] = read_qual
                out_row['start_time'] = self.start_time
                out_row['end_time'] = self.end_time
                out_row['contig_id'] = cid
                fout.write("{}".format("\t".join([str(x) for x in out_row.values()])))

        fout.close()