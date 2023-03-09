#!/usr/bin/env python
from filter_ONT.__init__ import check_ont_summary_file, Parser, Sequence
from filter_ONT.seq_summary_processing import SeqSummaryProcesser
from filter_ONT.seqtk import SeqtkRunner
seq_summary_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/sequencing_summary_FAT53867_9a53b23a.txt"
path_output = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/filter_ONT"
technology = "ONT"

invalid_seq_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/invalid_input.fastq"
path_enriched_test_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/Test_br1_sal_lam_enriched.fastq"
test_csv = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/test_output_unblocked_ids.csv"

# def test_seq_summary_validation():
#     assert check_ont_summary_file(seq_summary_file) == True
#     pass

# def test_seq_summary_parser():
#     parsed_object = Parser(seq_summary_file, "seq_summary")
#     assert parsed_object.seq_summary_file is not None
#     pass

# def test_seq_summary_processor():
#     parsed_object = Parser(seq_summary_file, "seq_summary")
#     seq_summary_process = SeqSummaryProcesser(parsed_object, path_output, "run1", classification = "no_decision",
#                                                min_ch = 1, max_ch = 69, min_start_time=1355, max_q = 3, min_dur=3)
#     seq_summary_process.generate_read_ids()
#     assert seq_summary_process.status == True
#     pass

def test_run_seqtk_unblocked():
    enriched_sample = Sequence(technology, [path_enriched_test_file])
    seqtk_run = SeqtkRunner(enriched_sample, test_csv, path_output, "test_output")
    seqtk_run.subset_fastq()
    assert seqtk_run.status == True
    pass
