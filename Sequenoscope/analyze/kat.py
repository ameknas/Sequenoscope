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
    def __init__(self, input_path, ref_path, out_path):
        self.input_path = input_path
        self.ref_path = ref_path
        self.out_path = out_path

    def kat_sect(self):
        input_fastq = self.input_path.out_files
        ref_fasta = self.ref_path
        out_file_sect = os.path.join(self.out_path, "output.tsv")
        kat_sect_cmd = "kat sect -o {} {} {}".format(out_file_sect, ref_fasta, input_fastq)
        (self.stdout, self.stderr) = run_command(kat_sect_cmd)
        return self.check_files(out_file_sect)

    def kat_filter(self):
        ref_fasta = self.ref_path
        out_file_hash = os.path.join(self.out_path, "kat_generated_hash.kmer")
        hash_build_command = "kat filter kmer -o {} {}".format(out_file_hash, ref_fasta)
        run_command(hash_build_command)

        input_fastq = self.input_path.out_files
        out_file_filter = os.path.join(self.out_path, "kat_filtered.fastq")
        filter_from_hash_cmd = "kat filter seq -o {} --seq {} {}".format(out_file_filter, input_fastq, out_file_hash)
        (self.stdout, self.stderr) = run_command(filter_from_hash_cmd)
        return self.check_files(out_file_filter)

    def kat_hist(self):
        input_fastq = self.input_seq.out_files
        out_file_hist = os.path.join(self.out_path, "hist_file.hist")
        kat_hist_cmd = "kat hist -o {} {}".format(out_file_hist, input_fastq)
        (self.stdout, self.stderr) = run_command(kat_hist_cmd)
        return self.check_files(out_file_hist)

    def check_files(self, output_file):
        if not os.path.isfile(output_file):
            return False
        elif os.path.getsize(output_file) == 0:
            return False
        else:
            return True



sample1 = Sequence("Illumina", ["reads1.fasta", "reads2.fasta"])
kat_run = kat_analysis(sample1, ref)
status = kat_run.kat_sect()


