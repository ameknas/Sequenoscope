#!/usr/bin/env python
import argparse as ap
from filter_ONT.__init__ import Parser, Sequence
from filter_ONT.seq_summary_processing import SeqSummaryProcesser
from filter_ONT.seqtk import SeqtkRunner

parser = ap.ArgumentParser(prog="sequenoscope", usage="%(prog)s <command> <argument>", description="%(prog)s version 1.0: a tool for analyzing and processing sequencing data.",
                           formatter_class= ap.RawTextHelpFormatter)

parser._positionals.title = "Commands"
parser._optionals.title = "Help"
subparsers = parser.add_subparsers()

analyze_parser = subparsers.add_parser('analyze', help='map reads to a target and produce a report with sequencing statistics')

plot_parser = subparsers.add_parser('plot', help='generate plots based on fastq or kmer hash files')


filter_parser = subparsers.add_parser('filter_ONT', help='filter reads from a fastq file based on a sequencing summary file')
filter_parser.usage = "sequenoscope filter_ONT --input_fastq <file.fq> --input_summary <seq_summary.txt> -o <out.fastq> [options]"
filter_parser._optionals.title = "Arguments"
filter_parser.formatter_class = ap.RawTextHelpFormatter
filter_parser.add_argument("--input_fastq", metavar="", required=True, nargs="+", help="[REQUIRED] Path to adaptive sequencing fastq files to process.")
filter_parser.add_argument("--input_summary", metavar="", required=True, help="[REQUIRED] Path to ONT sequencing summary file.")
filter_parser.add_argument("-o", "--output", metavar="", required=True, help="[REQUIRED] Output directory/file designation")
filter_parser.add_argument("-cls", "--classification", default= "all", metavar="", type= str, choices=['all', 'unblocked', 'stop_receiving', 'no_decision'], help="a designation of the adaptive-sampling sequencing decision classification ['unblocked', 'stop_receiving', or 'no_decision']")
filter_parser.add_argument("-min_ch", "--minimum_channel", default= 1, metavar="", type=int, help="a designation of the minimum channel/pore number for filtering reads")
filter_parser.add_argument("-max_ch", "--maximum_channel", default= 512, metavar="", type=int, help="a designation of the maximum channel/pore number for filtering reads")
filter_parser.add_argument("-min_dur", "--minimum_duration", default= 0, metavar="", type=float, help="a designation of the minimum duration of the sequencing run in SECONDS for filtering reads")
filter_parser.add_argument("-max_dur", "--maximum_duration", default= 100, metavar="", type=float, help="a designation of the maximum duration of the sequencing run in SECONDS for filtering reads")
filter_parser.add_argument("-min_start", "--minimum_start_time", default= 0, metavar="", type=float, help="a designation of the minimum start time of the sequencing run in SECONDS for filtering reads")
filter_parser.add_argument("-max_start", "--maximum_start_time", default= 259200,metavar="", type=float, help="a designation of the maximum start time of the sequencing run in SECONDS for filtering reads")
filter_parser.add_argument("-min_q", "--minimum_q_score", metavar="", default= 0, type=int, help="a designation of the minimum q score for filtering reads")
filter_parser.add_argument("-max_q", "--maximum_q_score", metavar="", default= 100, type=int, help="a designation of the maximum q score for filtering reads")
filter_parser.add_argument("-min_len", "--minimum_length", metavar="", default= 0, type=int, help="a designation of the minimum read length for filtering reads")
filter_parser.add_argument("-max_len", "--maximum_length", metavar="", default= 50000,type=int, help="a designation of the maximum read length for filtering reads")
args = parser.parse_args()
input_fastq = args.input_fastq
input_summary = args.input_summary
out_directory = args.output
as_class = args.classification
min_ch = args.minimum_channel
max_ch = args.maximum_channel
min_dur = args.minimum_duration
max_dur = args.maximum_duration
min_start = args.minimum_start_time
max_start = args.maximum_start_time
min_q = args.minimum_q_score
max_q = args.maximum_q_score
min_len = args.minimum_length
max_len = args.maximum_length

## parsing seq summary file

seq_summary_parsed = Parser(input_summary, "seq_summary")

## producing read list

seq_summary_process = SeqSummaryProcesser(seq_summary_parsed, out_directory, "read_id_list", classification= as_class, 
                                          min_ch=min_ch, max_ch=max_ch, min_dur=min_dur, max_dur=max_dur, min_start_time=min_start,
                                          max_start_time=max_start, min_q=min_q, max_q=max_q, min_len=min_len, max_len=max_len)

seq_summary_process.generate_read_ids()

## producing fastq via seqtk

sequencing_sample = Sequence("ONT", list_of_seq=[input_fastq])
seqtk_subset = SeqtkRunner(sequencing_sample, "read_id_list.csv", out_directory, "filtered_fastq")
seqtk_subset.subset_fastq()

