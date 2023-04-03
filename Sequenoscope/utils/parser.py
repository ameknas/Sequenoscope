#!/usr/bin/env python
from Sequenoscope.utils.__init__ import is_non_zero_file
import pandas as pd
import json
import re
import os

class GeneralSeqParser:
    file = None
    file_type = None
    parsed_file = None
    
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
            self.file_parsing_precheck(file, list_of_headers=["read_id", "channel", "start_time", "duration", "sequence_length_template", "mean_qscore_template", "end_reason"] )
            self.parse_seq_summary()
        pass

    def parse_tsv(self):
        self.parsed_file = pd.read_csv(self.file, sep='\t', header=0, index_col=0)
        

    def parse_json(self):
        self.parsed_file = json.load(open(self.file))

    def parse_csv(self):
        self.parsed_file = pd.read_csv(self.file)

    def parse_seq_summary(self):
        self.parsed_file = pd.read_csv(self.file, sep='\t', index_col=0)
        self.parsed_file = self.parsed_file[["read_id", "channel", "start_time", "duration", "sequence_length_template", "mean_qscore_template", "end_reason"]]
        self.parsed_file.reset_index(drop=True, inplace=True)

    def file_parsing_precheck(self, file_path, delemiter="\t", list_of_headers=None):
        if not is_non_zero_file(file_path):
            raise ValueError("Error: file not found")
        
        df = pd.read_csv(file_path, delimiter=delemiter)

        if list_of_headers is not None:
            if not set(list_of_headers).issubset(set(df.columns)):
                raise ValueError("Error: column headers did not match expected output. check file.")
        
        return True
    
class fastq_parser:
    REGEX_GZIPPED = re.compile(r'^.+\.gz$')
    f = None
    def __init__(self,filepath):
        self.filepath = filepath

    def parse(self):
        filepath  = self.filepath
        if self.REGEX_GZIPPED.match(filepath):
            # using os.popen with zcat since it is much faster than gzip.open or gzip.open(io.BufferedReader)
            # http://aripollak.com/pythongzipbenchmarks/
            # assumes Linux os with zcat installed
            with os.popen('zcat < {}'.format(filepath)) as f:
                yield from self.parse_fastq(f)
        else:
            with open(filepath, 'r') as f:
                yield from self.parse_fastq(f)
        return


    def parse_fastq(self,f):

        record = []
        n = 0
        for line in f:
            n += 1
            record.append(line.rstrip())
            if n == 4:
                yield record
                n = 0
                record = []