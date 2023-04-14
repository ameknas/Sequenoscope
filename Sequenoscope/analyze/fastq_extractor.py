#!/usr/bin/env python
import os

class FastqExtractor:
   
    status = False
    
    def __init__(self, out_prefix, out_dir):
        self.reads = []
        self.out_prefix = out_prefix
        self.out_dir = out_dir
   
    def extract_single_reads(self, fastq_file):
        output_file = os.path.join(self.out_dir,"{}.txt".format(self.out_prefix))
        with open(fastq_file, 'r') as f:
            for line in f:
                if line.startswith('@'):
                    if len(line.strip().split()) >= 4:
                        read_id = line.strip().split(" ")[0][1:]
                        self.reads.append(read_id)
        with open(output_file, 'w') as f:
            f.write("read_id\n")  # Write the header row
            for read in self.reads:
                f.write(f"{read}\n")
        self.status = self.check_files(output_file)
        if self.status == False:
            self.error_messages = "one or more files was not created or was empty, check error message\n{}".format(self.stderr)
            raise ValueError(str(self.error_messages))
               
    def extract_paired_reads(self, forward_file, reverse_file):
        output_file = os.path.join(self.out_dir,"{}.txt".format(self.out_prefix))
        forward_reads = []
        with open(forward_file, 'r') as f:
            for line in f:
                if line.startswith('@'):
                    if len(line.strip().split(":")) >= 4:
                        read_id = line.strip().split()[0][1:] #+ '_R1'
                        forward_reads.append(read_id)
        reverse_reads = []
        with open(reverse_file, 'r') as f:
            for line in f:
                if line.startswith('@'):
                    if len(line.strip().split(":")) >= 4:
                        read_id = line.strip().split()[0][1:] #+ '_R2'
                        reverse_reads.append(read_id)
        with open(output_file, 'w') as f:
            f.write("read_id\n")  # Write the header row
            for read in forward_reads + reverse_reads:
                f.write(f"{read}\n")
        self.status = self.check_files(output_file)
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