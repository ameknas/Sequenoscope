#!/usr/bin/env python
from analyze.__init__ import Sequence2, is_non_zero_file, compute_sha256
from analyze.kat import kat_analysis
import pytest

path_ref_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/lambda_genome_reference.fasta"
path_enriched_test_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/Test_br1_sal_lam_enriched.fastq"
path_control_test_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/Test_br1_sal_lam_control.fastq"
path_output = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze"
technology = "ONT"

invalid_ref_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/invalid_reference.fasta"
invalid_seq_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/invalid_input.fastq"

working_file_directory = "/mnt/c/Users/ameknas/Desktop/kat_hist_tests/kat_py_3.8.10/3.8.5/3.5"



def test_make_test():
    print ("hello world")
    pass

def compare_files():
    working_kat_sha = compute_sha256("/mnt/c/Users/ameknas/Desktop/kat_hist_tests/kat_py_3.8.10/3.8.5/3.5/histogram_file.png")
    kat_error_sha = compute_sha256("/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/histogram_file.png")
    assert working_kat_sha == kat_error_sha


# def test_kat_sect():
#     enriched_sample = Sequence2(technology, path_enriched_test_file)
#     kat_run = kat_analysis(enriched_sample, path_ref_file, path_output)
#     kat_run.kat_sect()
#     assert kat_run.status == True
#     pass

# def test_kat_filter():
#     enriched_sample = Sequence2(technology, path_enriched_test_file)
#     kat_run = kat_analysis(enriched_sample, path_ref_file, path_output)
#     kat_run.kat_filter()
#     assert kat_run.status == True
#     pass

# def test_kat_hist_Error():
#     enriched_sample = Sequence2(technology, path_enriched_test_file)
#     kat_run = kat_analysis(enriched_sample, path_ref_file, path_output)
#     with pytest.raises(ValueError) as exp:
#         kat_run.kat_hist()
#     assert str(exp.value) == "one or more files was not created or was empty, check error message\ncorrupted double-linked list\nAborted\n"

#-----------------------------

# def test_unsupported_file_format():
#     enriched_sample = Sequence2(technology, invalid_seq_file)
#     kat_run = kat_analysis(enriched_sample, invalid_ref_file, path_output)
#     with pytest.raises(ValueError) as exp:
#         kat_run.kat_sect()
#     assert str(exp.value) == "one or more files was not created or was empty, check error message\nError: Unsupported format\n"

#     with pytest.raises(ValueError) as exp:
#         kat_run.kat_filter()
#     assert str(exp.value) == "one or more files was not created or was empty, check error message\nError: Unsupported format\n"

# def test_supported_file_format():
#     enriched_sample = Sequence2(technology, path_enriched_test_file)
#     kat_run = kat_analysis(enriched_sample, path_ref_file, path_output)
#     kat_run.kat_sect()
#     assert kat_run.status == True

#     kat_run.kat_filter
#     assert kat_run.status == True
#     pass

# -------------------------------------------------------

# @pytest.fixture(scope="function")
# def load_seq_data():
#     enriched_sample = Sequence2(technology, path_enriched_test_file)
#     kat_run = kat_analysis(enriched_sample, path_ref_file, path_output)
#     yield kat_run

@pytest.mark.parametrize("kmer_size, file_produced", [
    ("27", "kat_generated_hash-in.jf27"),
    ("45","kat_generated_hash-in.jf45"),
    ("77","kat_generated_hash-in.jf77")
    ])
def test_kat_filter(kmer_size, file_produced):
    enriched_sample = Sequence2(technology, path_enriched_test_file)
    kat_run = kat_analysis(enriched_sample, path_ref_file, path_output, kmersize=kmer_size)
    kat_run.kat_filter()
    assert kat_run.status == True
    assert is_non_zero_file(file_produced) == True
    pass