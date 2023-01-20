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
    input_path = None
    ref_path = None
    out_path = None
    result_files = {"sect":{"cvg":"", "tsv":""}, "filter":{"jf27":"", "filtered_fastq":""}, "hist":{"hist_file":""}}
    error_messages = None
    status = False
    threads = 1

    def __init__(self, input_path, ref_path, out_path, threads = 1):
        """
        Initalize the class with input path, ref_path, and output path

        Arguments:
            input_path: sequence object
                an object that contains the list of sequence files for analysis
            ref_path: str
                a string to the path of reference sequence file
            out_path: str
                a string to the path where the output files will be stored
        """
        self.input_path = input_path
        self.ref_path = ref_path
        self.out_path = out_path
        self.threads = threads

    def kat_sect(self):
        """
        Run the kat sect command on the input sequences and reference sequence.

        Returns: 
            bool:
                returns True if the generated output file is found and not empty, False otherwise
        """
        input_fastq = self.input_path.out_files
        ref_fasta = self.ref_path
        out_file_sect = os.path.join(self.out_path, "output")
        cvg_file = os.path.join(out_file_sect, ".cvg")
        tsv_file = os.path.join(out_file_sect, ".tsv")

        self.result_files["sect"]["cvg"] = cvg_file
        self.result_files["sect"]["tsv"] = tsv_file

        kat_sect_cmd = "kat sect -t {} -o {} {} {}".format(self.threads, out_file_sect, ref_fasta, input_fastq)
        (self.stdout, self.stderr) = run_command(kat_sect_cmd)
        self.status = self.check_files([cvg_file, tsv_file])
        if self.status == False:
            self.error_messages = "one or more files was not created or was empty, check error message/n{}".format(self.stderr)

    def kat_filter(self):
        """
        Run the kat filter kmer command on the reference sequence to generate a kmer hash table and kat filter seq commmand
        on the input sequences along with the kat filter kmer hash table.

        Returns:
            bool:
                returns True if the generated output file is found and not empty, False otherwise
        """
        ref_fasta = self.ref_path
        out_file_hash = os.path.join(self.out_path, "kat_generated_hash")
        jf27_file = os.path.join(out_file_hash, ".jf27")

        self.result_files["filter"]["jf27"] = jf27_file

        hash_build_command = "kat filter kmer -o {} {}".format(out_file_hash, ref_fasta)
        run_command(hash_build_command)

        input_fastq = self.input_path.out_files
        out_file_filter = os.path.join(self.out_path, "kat_filtered")
        filtered_fastq_file = os.path.join(out_file_filter, ".fastq")

        self.result_files["filter"]["filtered_fastq"] = filtered_fastq_file

        filter_from_hash_cmd = "kat filter seq -t {} -o {} --seq {} {}".format(self.threads, out_file_filter, input_fastq, out_file_hash)
        (self.stdout, self.stderr) = run_command(filter_from_hash_cmd)
        self.status = self.check_files([jf27_file, filtered_fastq_file])
        if self.status == False:
            self.error_messages = "one or more files was not created or was empty, check error message/n{}".format(self.stderr)


    def kat_hist(self):
        """
        Run the kat hist command on the input file sequences

        Returns:
            bool:
                returns True if the generated output file is found and not empty, False otherwise
        """
        input_fastq = self.input_seq.out_files
        out_file_hist = os.path.join(self.out_path, "histogram_file")
        hist_generated_file = os.path.join(out_file_hist, ".txt")

        self.result_files["hist"]["hist_file"] = hist_generated_file
        
        kat_hist_cmd = "kat hist -t {} -o {} {}".format(self.threads, out_file_hist, input_fastq)
        (self.stdout, self.stderr) = run_command(kat_hist_cmd)
        self.status = self.check_files([hist_generated_file])
        if self.status == False:
            self.error_messages = "one or more files was not created or was empty, check error message/n{}".format(self.stderr)

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



sample1 = Sequence("Illumina", ["reads1.fasta", "reads2.fasta"])
kat_run = kat_analysis(sample1, ref)
kat_run.kat_sect()
if kat_run.status:
    print("hooray")
else:
    print("oh no!")
    print(kat_run.error_messages)
    exit()


