#!/usr/bin/env python
import os

class FastqExtractor:
    out_prefix = None
    out_dir = None
    read_set = None
    status = False
    result_files = {"read_list_file":""}
    
    def __init__(self, read_set, out_prefix, out_dir):
        """
        Initalize the class with read_set, out_prefix, and out_dir

        Arguments:
            read_set: sequence object
                an object that contains the list of sequence files for analysis
            out_prefix: str
                a designation of what the output files will be named
            out_dir: str
                a string to the path where the output files will be stored
        """
        self.reads = []
        self.out_prefix = out_prefix
        self.out_dir = out_dir
        self.read_set = read_set
   
    def extract_single_reads(self):
        """
        Extracts the read ids from a single-end fastq file based on the paramters intialized in the previous method.

        Returns:
            bool:
                returns True if the generated output file is found and not empty, False otherwise
        """
        output_file = os.path.join(self.out_dir,"{}.txt".format(self.out_prefix))
        self.result_files["read_list_file"] = output_file

        with open(self.read_set.files[0], 'r') as f:
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
               
    def extract_paired_reads(self):
        """
        Extracts the read ids from a paired-end fastq file based on the paramters intialized in the previous method.

        Returns:
            bool:
                returns True if the generated output file is found and not empty, False otherwise
        """
        output_file = os.path.join(self.out_dir,"{}.txt".format(self.out_prefix))
        self.result_files["read_list_file"] = output_file
        
        forward_reads = []
        with open(self.read_set.files[0], 'r') as f:
            for line in f:
                if line.startswith('@'):
                    if len(line.strip().split(":")) >= 4:
                        read_id = line.strip().split()[0][1:] #+ '_R1'
                        forward_reads.append(read_id)
        reverse_reads = []
        with open(self.read_set.files[1], 'r') as f:
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
        
    def alt_extract_paired_reads(self):
        """
        Extracts the read ids from a paired-end fastq file based on the paramters intialized in the previous method.

        Returns:
            bool:
                returns True if the generated output file is found and not empty, False otherwise
        """
        output_file = os.path.join(self.out_dir,"{}.txt".format(self.out_prefix))
        self.result_files["read_list_file"] = output_file
        
        forward_reads = []
        with open(self.read_set.files[0], 'r') as f:
            for line in f:
                if line.startswith('@'):
                    if line.endswith('1\n'):
                        read_id = line.strip().split()[0][1:] #+ '_R1'
                        forward_reads.append(read_id)
        reverse_reads = []
        with open(self.read_set.files[1], 'r') as f:
            for line in f:
                if line.startswith('@'):
                    if line.endswith('2\n'):
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