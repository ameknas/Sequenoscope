#!/usr/bin/env python
from analyze.__init__ import Sequence, Parser
from analyze.kat import KatRunner
from analyze.fastP import FastPRunner
from analyze.minimap2 import Minimap2Runner
from analyze.processing import SamBamProcessor, ASReportProcessor
from analyze.seqtk import SeqtkRunner


path_ref_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/lambda_genome_reference.fasta"
path_enriched_test_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/Test_br1_sal_lam_enriched.fastq"
path_control_test_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/Test_br1_sal_lam_control.fastq"
path_output = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze"
technology = "ONT"

invalid_ref_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/invalid_reference.fasta"
invalid_seq_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/invalid_input.fastq"

tsv_test_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/output-stats.tsv"
json_test_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/histogram_file.dist_analysis.json"
sam_test_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/test_output.sam"
bam_test_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/test_output.bam"
AS_report_test_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/adaptive_sampling_report.csv"
UB_csv_test_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/test_output_unblocked_ids.csv"
SR_csv_test_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/test_output_stop_receiving.csv"
ND_csv_test_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/test_output_no_decision.csv"


def test_make_test():
    print ("hello world")
    pass

# def test_kat_sect():
#     enriched_sample = Sequence(technology, [path_enriched_test_file, path_enriched_test_file])
#     kat_run = KatRunner(enriched_sample, path_ref_file, path_output)
#     kat_run.kat_sect()
#     assert kat_run.status == True
#     pass

# def test_kat_filter():
#     enriched_sample = Sequence(technology, [path_enriched_test_file, path_enriched_test_file])
#     kat_run = KatRunner(enriched_sample, path_ref_file, path_output)
#     kat_run.kat_filter(exclude=True)
#     assert kat_run.status == True
#     pass

# def test_kat_hist():
#     enriched_sample = Sequence(technology, [path_enriched_test_file])
#     kat_run = KatRunner(enriched_sample, path_ref_file, path_output)
#     kat_run.kat_hist()
#     assert kat_run.status == True
#     pass

# def test_kat_run_all():
#     enriched_sample = Sequence(technology, [path_enriched_test_file, path_enriched_test_file])
#     kat_run = KatRunner(enriched_sample, path_ref_file, path_output)
#     kat_run.run_all()
#     assert kat_run.status == True
#     pass

# def test_parser():
#     tsv_df = Parser(tsv_test_file, "tsv")
#     json_dict = Parser(json_test_file, "json")
#     pass


# def test_run_fastp(): 
#     enriched_sample = Sequence(technology, [path_enriched_test_file, path_enriched_test_file])
#     fastp_run = FastPRunner(enriched_sample, path_output, "test_output", "test_output_2", report_only=False, dedup=True)
#     fastp_run.run_fastp()
#     assert fastp_run.status == True
#     pass

# def test_run_minimap2(): 
#     enriched_sample = Sequence(technology, [path_enriched_test_file, path_enriched_test_file])
#     minimap2_run = Minimap2Runner(enriched_sample, path_output, path_ref_file, "test_output")
#     minimap2_run.run_minimap2()
#     assert minimap2_run.status == True
#     pass

# def test_run_samtools_bam(): 
#     samtools_run = SamBamProcessor(sam_test_file, path_output, path_ref_file, "test_output")
#     samtools_run.run_samtools_bam(exclude=True)
#     assert samtools_run.status == True
#     pass

# def test_run_samtools_fastq(): 
#     samtools_run = SamBamProcessor(bam_test_file, path_output, path_ref_file, "test_output")
#     samtools_run.run_samtools_fastq()
#     assert samtools_run.status == True
#     pass

# def test_run_bedtools(): 
#     bedtools_run = SamBamProcessor(bam_test_file, path_output, path_ref_file, "test_output")
#     bedtools_run.run_bedtools(nonzero=True)
#     assert bedtools_run.status == True
#     pass

# def test_run_generate_unblocked():
#     parsed_file = Parser(AS_report_test_file, "csv")
#     unblocked_run = ASReportProcessor(parsed_file, path_output, "test_output")
#     unblocked_run.generate_unblocked()
#     assert unblocked_run.status == True
#     pass

# def test_run_generate_stop_receiving():
#     parsed_file = Parser(AS_report_test_file, "csv")
#     stop_receiving_run = ASReportProcessor(parsed_file, path_output, "test_output")
#     stop_receiving_run.generate_stop_receiving()
#     assert stop_receiving_run.status == True
#     pass

# def test_run_generate_no_decision():
#     parsed_file = Parser(AS_report_test_file, "csv")
#     no_decision_run = ASReportProcessor(parsed_file, path_output, "test_output")
#     no_decision_run.generate_no_decision()
#     assert no_decision_run.status == True
#     pass

def test_run_seqtk_unblocked():
    enriched_sample = Sequence(technology, [path_enriched_test_file])
    seqtk_UB_subet_run = SeqtkRunner(enriched_sample, UB_csv_test_file, path_output, "test_output")
    seqtk_UB_subet_run.subset_fastq()
    assert seqtk_UB_subet_run.status == True
    pass






