from analyze import run_command
from analyze import Sequence
import os

def kat_sect(input_fastq, ref_seq):
    kat_command = "kat sect -o output.tsv " + ref_seq + " " + input_fastq
    run_command(kat_command)

def kat_filter(input_fastq, ref_seq):
    #generate a hash table based on ref fasta file
    hash_build = "kat filter kmer -o kat_generated_hash.kmer" + ref_seq
    run_command(hash_build)
    #analyze based on generated hash
    filter_from_hash = "kat filter seq -o kat_filtered.fastq --seq " + input_fastq + " kat_generated_hash.kmer"
    run_command(filter_from_hash)

ref = "ref.fasta"

class kat_analysis:
    def __init__(self, input_seq, ref_seq):
        self.input_seq = Sequence(input_seq.technology, input_seq.files)
        self.ref_seq = ref

    def kat_sect(self):
        input_fastq = self.input_seq.out_files
        ref_fasta = self.ref_seq
        kat_sect_cmd = "kat sect -o output.tsv" + ref_fasta + " " + input_fastq
        run_command(kat_sect_cmd)
        self.check_for_errors("output.tsv")

    def kat_filter(self):
        input_fastq = self.input_seq.out_files
        ref_fasta = self.ref_seq
        hash_build_command = "kat filter kmer -o kat_generated_hash.kmer" + ref_fasta
        run_command(hash_build_command)
        filter_from_hash_cmd = "kat filter seq -o kat_filtered.fastq --seq " + input_fastq + " kat_generated_hash.kmer"
        run_command(filter_from_hash_cmd)
        self.check_for_errors("kat_filtered.fastq")

    def kat_hist(self):
        input_fastq = self.input_seq.out_files
        kat_hist_cmd = "kat hist -o hist_file.hist" + input_fastq
        run_command (kat_hist_cmd)
        self.check_for_errors("hist_file.hist")

    def check_for_errors(self, output_file):
        if run_command.stdout != 0:
            print("Error: ", run_command.stderr)
            exit()
        elif os.path.getsize (output_file):
            print("Error: ", output_file, "is an empty file")
            exit()


