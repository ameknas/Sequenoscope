#!/usr/bin/env python
from Sequenoscope.utils.__init__ import run_command
from Sequenoscope.utils.parser import GeneralSeqParser
from Sequenoscope.utils.sequence_class import Sequence
import os
import pandas as pd



class SamBamProcessor:
    file = None
    out_dir = None
    out_prefix = None
    ref_database = None
    threads = 1
    status = False
    error_messages = None
    result_files = {"bam_output":"", "fastq_output":"", "coverage_tsv":""}
    
    
    def __init__(self, file, out_dir, ref_database, out_prefix, thread=1):
        """
        Initalize the class with read_set, out_dir, ref_database, and out_prefix

        Arguments:
            file: str
                path to sam or bam file for processing
            out_dir: str
                a string to the path where the output files will be stored
            ref_database: str
                a string to the path of reference sequence file
            out_prefix: str
                a designation of what the output files will be named
            threads: int
                an integer representing the number of threads utilized for the operation, default is 1
        """
        self.file = file
        self.out_dir = out_dir
        self.ref_database = ref_database
        self.out_prefix = out_prefix
        self.threads = thread

    def run_samtools_bam(self, exclude=False):
        """
        Run the samtools view command on the designated sam file and pipe the output to the samtools sort command for further processing.

        Arguments:
            exclude: bool
                returns all mapped reads if True, and returns all unmapped reads if False

        Returns:
            bool:
                returns True if the generated output file is found and not empty, False otherwise
        """
        bam_output = os.path.join(self.out_dir,"{}.bam".format(self.out_prefix))
        
        self.result_files["bam_output"] = bam_output
        
        cmd = ["samtools", "view", "-S", "-b", "4", self.file, "|",
               "samtools", "sort", "-@", "{}".format(self.threads), "-T", self.out_prefix, "--reference", self.ref_database,
               "-o", bam_output]

        if exclude == True:
            cmd.insert(4, "-f")
        else:
            cmd.insert(4, "-F")

        cmd_string = " ".join(cmd)

        (self.stdout, self.stderr) = run_command(cmd_string)
        self.status = self.check_files([bam_output])
        if self.status == False:
            self.error_messages = "one or more files was not created or was empty, check error message\n{}".format(self.stderr)
            raise ValueError(str(self.error_messages))

    def run_samtools_fastq(self):
        """
        Run the samtools fastq command to convert the designated bam file to a fastq file

        Returns:
            bool:
                returns True if the generated output file is found and not empty, False otherwise
        """
        fastq_output = os.path.join(self.out_dir,"{}.fastq".format(self.out_prefix))

        self.result_files["fastq_output"] = fastq_output

        cmd = "samtools fastq {} > {}".format(self.file, fastq_output)

        (self.stdout, self.stderr) = run_command(cmd)
        self.status = self.check_files([fastq_output])
        if self.status == False:
            self.error_messages = "one or more files was not created or was empty, check error message\n{}".format(self.stderr)
            raise ValueError(str(self.error_messages))

    def run_bedtools(self, nonzero = False):
        """
        Run the bedtools genomcov command on the designated bam file and return a tsv of the depth per base

        Arguments:
            nonzero: bool
                returns only depths greater than zero if True, and returns all depths if False

        Returns:
            bool:
                returns True if the generated output file is found and not empty, False otherwise
        """
        coverage_tsv = os.path.join(self.out_dir,"{}.tsv".format(self.out_prefix))

        self.result_files["coverage_tsv"] = coverage_tsv

        cmd = ["bedtools", "genomecov", "-ibam", self.file, ">", coverage_tsv]

        if nonzero == True:
            cmd.insert(4, "-dz")
        else:
            cmd.insert(4, "-d")

        cmd_string = " ".join(cmd)

        (self.stdout, self.stderr) = run_command(cmd_string)
        self.status = self.check_files([coverage_tsv])
        if self.status == False:
            self.error_messages = "one or more files was not created or was empty, check error message\n{}".format(self.stderr)
            raise ValueError(str(self.error_messages))


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

class ASReportProcessor:
    parsed_report_object = None
    out_dir = None
    out_prefix = None
    status = False
    error_messages = None
    result_files = {"unblocked_ids":"", "stop_receiving_ids":"", "no_decision":""}

    def __init__(self, parsed_report_object, out_dir, out_prefix):
        """
        Initalize the class with parsed_report_object, out_dir, and out_prefix

        Arguments:
            parsed_report_object: parser object
                an object that contains the parsed adaptive sampling report for analysis
            ref_database: str
                a string to the path of reference sequence file
            out_prefix: str
                a designation of what the output files will be named
        """
        self.parsed_report_object = parsed_report_object.csv_file
        self.out_dir = out_dir
        self.out_prefix = out_prefix
        pass

    def generate_unblocked(self):
        """
        generate a csv file of unblocked reads based on the designation of the read in the adaptive sampling
        report

        Returns:
            bool:
                returns True if the generated output file is found and not empty, False otherwise
        """
        unblocked_ids_csv = os.path.join(self.out_dir,"{}_unblocked_ids.csv".format(self.out_prefix))

        self.result_files["unblocked_ids"] = unblocked_ids_csv

        unblock_df = self.parsed_report_object[self.parsed_report_object['decision'] == "unblock"]
        unblock_df = unblock_df[["read_id", "decision"]]
        unblock_ids = unblock_df[["read_id"]]

        unblock_ids.to_csv(unblocked_ids_csv, index=False)

        self.status = self.check_files([unblocked_ids_csv])
        if self.status == False:
            self.error_messages = "one or more files was not created or was empty"
            raise ValueError(str(self.error_messages))

    def generate_stop_receiving(self):
        """
        generate a csv file of stop_receiving reads based on the designation of the read in the adaptive sampling
        report

        Returns:
            bool:
                returns True if the generated output file is found and not empty, False otherwise
        """
        stop_receiving_csv = os.path.join(self.out_dir,"{}_stop_receiving.csv".format(self.out_prefix))

        self.result_files["stop_receiving_ids"] = stop_receiving_csv

        stop_df = self.parsed_report_object[self.parsed_report_object['decision'] == "stop_receiving"]
        stop_df = stop_df[["read_id", "decision"]]
        stop_recieving_ids = stop_df[["read_id"]]

        stop_recieving_ids.to_csv(stop_receiving_csv, index=False)

        self.status = self.check_files([stop_receiving_csv])
        if self.status == False:
            self.error_messages = "one or more files was not created or was empty"
            raise ValueError(str(self.error_messages))

    def generate_no_decision(self):
        """
        generate a csv file of no_decision reads based on the designation of the read in the adaptive sampling
        report. if the reads are repeated and later designated as stop_receiving or unblocked, the duplicated
        reads are removed from the final csv file.

        Returns:
            bool:
                returns True if the generated output file is found and not empty, False otherwise
        """
        no_decision_csv = os.path.join(self.out_dir,"{}_no_decision.csv".format(self.out_prefix))

        self.result_files["no_decision"] = no_decision_csv

        ids = self.parsed_report_object["read_id"]
        df_dup = self.parsed_report_object[ids.isin(ids[ids.duplicated()])].sort_values("read_id")
        no_decision_duplicate_df = df_dup[df_dup['decision'] == "no_decision"]
        no_decision_duplicate_df = no_decision_duplicate_df[["read_id"]]
        no_dec_list = no_decision_duplicate_df["read_id"].values.tolist()

        df_no_dup = self.parsed_report_object[~((self.parsed_report_object['decision'] == "no_decision") & (self.parsed_report_object['read_id'].isin(no_dec_list)))]
        no_decision_modified_df = df_no_dup[df_no_dup['decision'] == "no_decision"]
        no_decision_modified_df = no_decision_modified_df[["read_id", "decision"]]
        no_decision_no_dup_ids = no_decision_modified_df[["read_id"]]

        no_decision_no_dup_ids.to_csv(no_decision_csv, index=False)

        self.status = self.check_files([no_decision_csv])
        if self.status == False:
            self.error_messages = "one or more files was not created or was empty"
            raise ValueError(str(self.error_messages))

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

    pass       