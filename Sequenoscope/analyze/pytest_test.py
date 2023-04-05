#!/usr/bin/env python
from Sequenoscope.utils.sequence_class import Sequence
from Sequenoscope.utils.parser import GeneralSeqParser
from Sequenoscope.analyze.kat import KatRunner
from Sequenoscope.analyze.fastP import FastPRunner
from Sequenoscope.analyze.minimap2 import Minimap2Runner
from Sequenoscope.analyze.processing import SamBamProcessor
from Sequenoscope.analyze.bam import BamProcessor
from Sequenoscope.analyze.seq_manifest import SeqManifest

path_ref_file = "/home/ameknas/sequenoscope-1/Sequenoscope/analyze/test_sequences/lambda_genome_reference.fasta"
path_enriched_test_file = "/home/ameknas/sequenoscope-1/Sequenoscope/analyze/test_sequences/Test_br1_sal_lam_enriched.fastq"
path_control_test_file = "/home/ameknas/sequenoscope-1/Sequenoscope/analyze/test_sequences/Test_br1_sal_lam_control.fastq"
path_output = "/home/ameknas/sequenoscope-1/Sequenoscope/analyze"
technology = "ONT"

invalid_ref_file = "/home/ameknas/sequenoscope-1/Sequenoscope/analyze/test_sequences/invalid_reference.fasta"
invalid_seq_file = "/home/ameknas/sequenoscope-1/Sequenoscope/analyze/test_sequences/invalid_input.fastq"

tsv_test_file = "/home/ameknas/sequenoscope-1/Sequenoscope/analyze/test_sequences/output-stats.tsv"
json_test_file = "/home/ameknas/sequenoscope-1/Sequenoscope/analyze/test_sequences/histogram_file.dist_analysis.json"
sam_test_file = "/home/ameknas/sequenoscope-1/Sequenoscope/analyze/test_sequences/test_output.sam"
bam_test_file = "/home/ameknas/sequenoscope-1/Sequenoscope/analyze/test_sequences/test_output.bam"
AS_report_test_file = "/home/ameknas/sequenoscope-1/Sequenoscope/analyze/test_sequences/adaptive_sampling_report.csv"
UB_csv_test_file = "/home/ameknas/sequenoscope-1/Sequenoscope/analyze/test_sequences/test_output_unblocked_ids.csv"
SR_csv_test_file = "/home/ameknas/sequenoscope-1/Sequenoscope/analyze/test_sequences/test_output_stop_receiving.csv"
ND_csv_test_file = "/home/ameknas/sequenoscope-1/Sequenoscope/analyze/test_sequences/test_output_no_decision.csv"
cmd = "python -m Sequenoscope.main analzye --input_fastq /home/ameknas/sequenoscope-1/Sequenoscope/analyze/test_sequences/Test_br1_sal_lam_enriched.fastq --input_reference /home/ameknas/sequenoscope-1/Sequenoscope/analyze/test_sequences/invalid_reference.fasta -o test -seq_type sr -min_len 3 -trm_tail 100"
test_bam = "/home/ameknas/sequenoscope-1/test/sample_mapped_bam.bam"

def test_make_test():
    print ("hello world")
    pass

# def test_kat_sect():
#     enriched_sample = Sequence(technology, [path_enriched_test_file, path_enriched_test_file])
#     kat_run = KatRunner(enriched_sample, path_ref_file, path_output, "test")
#     kat_run.kat_sect()
#     assert kat_run.status == True
#     pass

# def test_kat_filter():
#     enriched_sample = Sequence(technology, [path_enriched_test_file, path_enriched_test_file])
#     kat_run = KatRunner(enriched_sample, path_ref_file, path_output, "test")
#     kat_run.kat_filter(exclude=True)
#     assert kat_run.status == True
#     pass

# def test_kat_hist():
#     enriched_sample = Sequence(technology, [path_enriched_test_file])
#     kat_run = KatRunner(enriched_sample, path_ref_file, path_output, "test")
#     kat_run.kat_hist()
#     assert kat_run.status == True
#     pass

# def test_run_fastp(): 
#     enriched_sample = Sequence(technology, [path_enriched_test_file])
#     fastp_run = FastPRunner(enriched_sample, path_output, "test_output", report_only=False, dedup=True)
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

# def test_run_samtools_import(): 
#     samtools_run = SamBamProcessor(path_enriched_test_file, path_output, path_ref_file, "test_output")
#     samtools_run.run_samtools_import()
#     assert samtools_run.status == True
#     pass

# def test_run_bedtools(): 
#     bedtools_run = SamBamProcessor(bam_test_file, path_output, path_ref_file, "test_output")
#     bedtools_run.run_bedtools(nonzero=True)
#     assert bedtools_run.status == True
#     pass

def test_run_bam(): 
    bam_run = BamProcessor("/home/ameknas/sequenoscope-1/test-sal/sample_mapped_bam.bam")
    reads = []
    for i in bam_run.ref_stats:
        num_reads = bam_run.ref_stats[i]['num_reads']
        reads.append(num_reads)
    print(sum(reads), file=open('test_reads_total.txt', 'a'))
    assert bam_run.status == True
    pass

# def test_run_seq_manifest_nanopore(): 
#     seq_mani_run = SeqManifest("barcode1",
#                                "/home/ameknas/sequenoscope-1/test-br1-alt/sample_mapped_bam.bam", 
#                                "out_mani_1", 
#                                fastp_fastq="/home/ameknas/sequenoscope-1/test-br1-alt/sample_fastp_output.fastp.fastq",
#                                in_seq_summary= "/home/ameknas/sequenoscope-1/Sequenoscope/analyze/test_sequences/sequencing_summary_FAT53867_9a53b23a.txt"
#                                )
#     assert seq_mani_run.status == True
#     pass