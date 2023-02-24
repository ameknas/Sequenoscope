#!/usr/bin/env python
import unittest
from analyze.__init__ import Sequence2
from analyze.kat import kat_analysis

path_ref_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/lambda_genome_reference.fasta"
path_enriched_test_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/Test_br1_sal_lam_enriched.fastq"
path_control_test_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/Test_br1_sal_lam_control.fastq"
path_output = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze"
technology = "ONT"

invalid_ref_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/invalid_reference.fasta"
invalid_seq_file = "/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/invalid_input.fastq"


class test_test(unittest.TestCase):
    def test_make_test(self):
     print ("hello world")

class test_kat_run(unittest.TestCase):
    def test_kat_sect(self):
        enriched_sample = Sequence2(technology, path_enriched_test_file)
        kat_run = kat_analysis(enriched_sample, path_ref_file, path_output)
        kat_run.kat_sect()
        assert kat_run.status == True
        pass

    def test_kat_filter(self):
        enriched_sample = Sequence2(technology, path_enriched_test_file)
        kat_run = kat_analysis(enriched_sample, path_ref_file, path_output)
        kat_run.kat_filter()
        assert kat_run.status == True
        pass
    
    # def test_kat_hist(self):
    #     enriched_sample = Sequence2(technology, path_enriched_test_file)
    #     kat_run = kat_analysis(enriched_sample, path_ref_file, path_output)
    #     kat_run.kat_hist()
    #     assert kat_run.status == True
    #     pass

    # def test_kat_hist(self):
    #     enriched_sample = Sequence(technology, path_enriched_test_file)
    #     kat_run = kat_analysis(enriched_sample, path_ref_file, path_output)
    #     kat_run.kat_hist()
    #     assert kat_run.status == True
    #     pass

    # def test_kat_all(self):
    #     enriched_sample = Sequence(technology, path_enriched_test_file)
    #     kat_run = kat_analysis(enriched_sample, path_ref_file, path_output)
    #     kat_run.run_all()
    #     pass

#class invalid_kat_run(unittest.TestCase):
#     def test_kat_sect(self):
#         enriched_sample = Sequence(technology, invalid_seq_file)
#         kat_run = kat_analysis(enriched_sample, invalid_ref_file, path_output)
#         kat_run.kat_sect()
#         pass

if __name__ == '__main__':
    unittest.main

# enriched_sample = Sequence2("Illumina", path_enriched_test_file)
# print(enriched_sample.out_files)

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


# kmer_27_sha = compute_sha256("/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/sha_kat_generated_hash-in.jf27")
# kmer_45_sha = compute_sha256("/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/sha_kat_generated_hash-in.jf45")
# kmer_77_sha = compute_sha256("/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/sha_kat_generated_hash-in.jf77")



# @pytest.mark.parametrize("kmer_size, file_produced", [
#     ("27","kat_generated_hash-in.jf27"),
#     ("45","kat_generated_hash-in.jf45"),
#     ("77","kat_generated_hash-in.jf77")
#     ])
# def test_kat_filter(kmer_size, file_produced):
#     enriched_sample = Sequence2(technology, path_enriched_test_file)
#     kat_run = kat_analysis(enriched_sample, path_ref_file, path_output, kmersize=kmer_size)
#     kat_run.kat_filter()
#     assert kat_run.status == True
#     assert is_non_zero_file(file_produced) == True
#     if file_produced == "kat_generated_hash-in.jf27":
#         assert compute_sha256(file_produced) == kmer_27_sha
#     if file_produced == "kat_generated_hash-in.jf45":
#         assert compute_sha256(file_produced) == kmer_45_sha
#     if file_produced == "kat_generated_hash-in.jf77":
#         assert compute_sha256(file_produced) == kmer_77_sha
#     pass



# def test_hash_same(files):
#     hashes = []
#     for file in files:
#         hash = compute_sha256(file)
#         hashes.append(hash)

#     for f in range(len(hashes)):
#         for i in range(f +1, len(hashes)):
#             assert hashes[f] != hashes[i], "{files[f]} and {files[i]} have the same hash: {hashes[i]}" 

# def test_kat_sect():
#      enriched_sample = Sequence(technology, [path_enriched_test_file, path_control_test_file])
#      assert enriched_sample.out_files == '/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/Test_br1_sal_lam_enriched.fastq /mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/Test_br1_sal_lam_control.fastq'
#      assert enriched_sample.is_paired == True

# def test_seq():
#      enriched_sample = Sequence(technology, [path_enriched_test_file])
#      assert enriched_sample.out_files == '/mnt/c/Users/ameknas/Desktop/Sequenoscope/Sequenoscope/sequenoscope/analyze/test_sequences/Test_br1_sal_lam_enriched.fastq'
#      assert enriched_sample.is_paired == False