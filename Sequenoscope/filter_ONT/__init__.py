#!/usr/bin/env python
from subprocess import Popen, PIPE
import os
import pandas as pd
import json

def run_command(command):
    p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    return stdout, stderr

def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

def check_ont_summary_file(file_path):
    if not os.path.isfile(file_path):
        raise ValueError("Error: file not found")
        

    with open(file_path, "r") as f:
        lines = f.readlines()

    if not lines or len(lines) < 2:
        raise ValueError("Error: file is empty or has fewer than 2 lines")
        
    
    for line in lines[1:]:
        fields = line.strip().split("\t")
        if len(fields) != 41:
            raise ValueError(f"Error: malformed line: {line.strip()}")
        try:
            int(fields[4])
        except ValueError:
            raise ValueError(f"Error: invalid channel designation: {fields[4]}")
    
    return True

class Sequence:
    technology = None
    files = []
    is_paired = False
    out_files = ''

    def __init__(self, tech_name, list_of_seq):
        self.technology = tech_name
        self.files = list_of_seq
        for file in self.files:
            if not self.is_fastq(file):
                raise ValueError(f'{file} is not a valid fastq file')
        self.classify_seq()
        self.output_formatted_files()
        return

    def classify_seq(self):
        if len(self.files) == 2:
            self.is_paired = True

    def is_fastq(self, input):
        with open(input, "r") as f:
            first_line = f.readline().strip()
            if not first_line.startswith("@"):
                return False

            second_line =  f.readline().strip()

            third_line = f.readline().strip()
            if not third_line.startswith("+"):
                return False
            
            fourth_line = f.readline().strip()

            if len(second_line) != len(fourth_line):
                return False
            
        return True

    def output_formatted_files(self):
        self.out_files = ' '.join(self.files)

class Parser:
    file = None
    file_type = None
    tsv_file = None
    json_file = None
    csv_file = None
    seq_summary_file = None
    
    def __init__(self, file, file_type):
        self.file = file
        self.file_type = file_type
        if file_type == "tsv":
            self.parse_tsv()
        if file_type == "json":
            self.parse_json()
        if file_type == "csv":
            self.parse_csv()
        if file_type == "seq_summary":
            self.parse_seq_summary()
        pass

    def parse_tsv(self):
        self.tsv_file = pd.read_csv(self.file, sep='\t', header=0, index_col=0)
        

    def parse_json(self):
        self.json_file = json.load(open(self.file))

    def parse_csv(self):
        self.csv_file = pd.read_csv(self.file)

    def parse_seq_summary(self):
        if check_ont_summary_file(self.file):
            self.seq_summary_file = pd.read_csv(self.file, sep='\t', index_col=0)
            self.seq_summary_file = self.seq_summary_file[["read_id", "channel", "start_time", "duration", "sequence_length_template", "mean_qscore_template", "end_reason"]]
            self.seq_summary_file.reset_index(drop=True, inplace=True)

