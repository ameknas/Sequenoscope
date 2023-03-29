#!/usr/bin/env python

import argparse as ap
import os
import sys
import time
from Sequenoscope.version import __version__
from Sequenoscope.utils.parser import GeneralSeqParser 
from Sequenoscope.utils.sequence_class import Sequence
from Sequenoscope.analyze.minimap2 import Minimap2Runner
from Sequenoscope.analyze.fastP import FastPRunner
from Sequenoscope.analyze.kat import KatRunner
from Sequenoscope.analyze.processing import SamBamProcessor

def parse_args():
    parser = ap.ArgumentParser(prog="sequenoscope",
                               usage="sequenoscope analyze --input_fastq <file.fq> --input_reference <ref.fasta> -o <out> -seq_type <sr>[options]\nFor help use: sequenoscope analyze -h or sequenoscope analyze --help", 
                                description="%(prog)s version {}: a tool for analyzing and processing sequencing data.".format(__version__), 
                                formatter_class= ap.RawTextHelpFormatter)

    parser._optionals.title = "Arguments"

    parser.add_argument("--input_fastq", metavar="", required=True, nargs="+", help="[REQUIRED] Path to fastq files to process.")
    parser.add_argument("--input_reference", metavar="", required=True, help="[REQUIRED] Path to reference database to process")
    parser.add_argument("-o", "--output", metavar="", required=True, help="[REQUIRED] Output directory designation")
    parser.add_argument("-o_pre", "--output_prefix", metavar="", default= "sample", help="Output file prefix designation. default is [sample]")
    parser.add_argument("-seq_type", "--sequencing_type", required=True, metavar="", type= str, choices=['sr', 'lr'], help="a designation of the type of sequencing utilized for the input fastq files")
    parser.add_argument("-t", "--threads", default= 1, metavar="", type=int, help="a designation of the number of threads to use")
    parser.add_argument("-kmer_s", "--kmer_size", default= 15, metavar="", type=int, help="a designation of the kmer size when mapping or processing")
    parser.add_argument("-min_len", "--minimum_read_length", default= 15, metavar="", type=int, help="a designation of the minimum read length. reads shorter than the integer specified required will be discarded, default is 15")
    parser.add_argument("-max_len", "--maximum_read_length", default= 0, metavar="", type=int, help="a designation of the maximum read length. reads longer than the integer specified required will be discarded, default is 0 meaning no limitation")
    parser.add_argument("-trm_fr", "--trim_front_bp", default= 0, metavar="", type=int, help="a designation of the how many bases to trim from the front of the sequence, default is 0.")
    parser.add_argument("-trm_tail", "--trim_tail_bp", default= 0,metavar="", type=int, help="a designation of the how many bases to trim from the tail of the sequence, default is 0")
    parser.add_argument('--exclude', required=False, help='choose to exclude reads based on reference instead of including them', action='store_true')
    parser.add_argument('--cov_nonzero', required=False, help='choose to include only nonzero values in coverage calculation', action='store_true')
    parser.add_argument('--force', required=False, help='Force overwite of existing results directory', action='store_true')
    parser.add_argument('-v', '--version', action='version', version="%(prog)s " + __version__)
    return parser.parse_args()

def run():
    args = parse_args()
    input_fastq = args.input_fastq
    input_reference = args.input_reference
    out_directory = args.output
    out_prefix = args.output_prefix
    seq_class= args.sequencing_type
    threads = args.threads
    kmer_size = args.kmer_size
    min_len = args.minimum_read_length
    max_len = args.maximum_read_length
    trim_front = args.trim_front_bp
    trim_tail = args.trim_tail_bp
    exclude = args.exclude
    force = args.force
    cov_nonzero = args.cov_nonzero

    print("-"*40)
    print("Sequenoscope analyze version {}: processing and analyzing reads based on given paramters".format(__version__))
    print("-"*40)

    ## intializing directory for files

    if not os.path.isdir(out_directory):
        os.mkdir(out_directory, 0o755)
    elif not force:
        print("Error directory {} already exists, if you want to overwrite existing results then specify --force".format(out_directory))
        sys.exit()

    ## parsing seq summary file

    print("-"*40)
    print("Processing sequence fastq file...")
    print("-"*40)

    sequencing_sample = Sequence("Test", input_fastq)

    ## filtering reads with fastp

    fastp_run_process = FastPRunner(sequencing_sample, out_directory, "{}_fastp_output".format(out_prefix), 
                                    min_read_len=min_len, max_read_len=max_len, trim_front_bp=trim_front,
                                    trim_tail_bp=trim_tail, report_only=False, dedup=False, threads=threads)

    
    fastp_run_process.run_fastp()

    ## mapping to reference via minimap2 and samtools

    print("-"*40)
    print("Mapping fastq based on the provided reference fasta file....")
    print("-"*40)

    sequencing_sample_filtered = Sequence("Test", fastp_run_process.result_files["output_files_fastp"])
    minimap_run_process = Minimap2Runner(sequencing_sample_filtered, out_directory, input_reference,
                                        "{}_mapped_sam".format(out_prefix), threads=threads,
                                        kmer_size=kmer_size)
    minimap_run_process.run_minimap2()

    sam_to_bam_process = SamBamProcessor(minimap_run_process.result_files["sam_output_file"], out_directory,
                                         input_reference, "{}_mapped_bam".format(out_prefix), thread=threads)
    sam_to_bam_process.run_samtools_bam(exclude=exclude)

    bam_to_fastq_process = SamBamProcessor(sam_to_bam_process.result_files["bam_output"], out_directory,
                                         input_reference, "{}_mapped_fastq".format(out_prefix), thread=threads)
    bam_to_fastq_process.run_samtools_fastq()

    bedtools_coverage_process = SamBamProcessor(sam_to_bam_process.result_files["bam_output"], out_directory,
                                         input_reference, "{}_bedtools_coverage".format(out_prefix), thread=threads)
    bedtools_coverage_process.run_bedtools(nonzero=cov_nonzero)

    print("-"*40)
    print("Analyzing kmers...")
    print("-"*40)

    # using kat hist to analyze kmers

    kat_run = KatRunner(sequencing_sample, input_reference, out_directory, "{}_kmer_analysis".format(out_prefix), kmersize = kmer_size)
    kat_run.kat_hist()


    print("-"*40)
    print("All Done!")
    print("-"*40)