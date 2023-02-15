from subprocess import Popen, PIPE
import os
import hashlib
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

def compute_sha256(file_name):
    hash_sha256 = hashlib.sha256()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(5000), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()     

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

    def is_fastq(self,input):
        return isinstance(input,str) or (input.endswith('.fastq')) or (input.endswith('.fq'))

    def output_formatted_files(self):
        self.out_files = ' '.join(self.files)

class Parser:
    file = None
    file_type = None
    tsv_file = None
    json_file = None
    csv_file = None
    
    def __init__(self, file, file_type):
        self.file = file
        self.file_type = file_type
        if file_type == "tsv":
            self.parse_tsv()
        if file_type == "json":
            self.parse_json()
        if file_type == "csv":
            self.parse_csv()
        pass

    def parse_tsv(self):
        self.tsv_file = pd.read_csv(self.file, sep='\t', header=0, index_col=0)

    def parse_json(self):
        self.json_file = json.load(open(self.file))

    def parse_csv(self):
        self.csv_file = pd.read_csv(self.file)


