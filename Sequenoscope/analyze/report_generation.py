#!/usr/bin/env python
import pandas as pd

class ReportGenerator:
    hist_json_file = None
    fastp_json_file = None
    bedtools_coverage_file = None
    bam_file = None
    result_values = []
    status = False
    error_messages = None

    def __init__(self, parsed_object_fastp_json, parsed_object_hist_json, parsed_object_bedtools_tsv, bam_file):
        self.fastp_json_file = parsed_object_fastp_json.parsed_file
        self.hist_json_file = parsed_object_hist_json.parsed_file
        self.bedtools_coverage_file = parsed_object_bedtools_tsv.parsed_file
        self.bam_file = bam_file
        ##run functions when class is intialized
        self.get_values_fastp()
        self.get_values_hist()
        self.get_values_bedtools()
        self.get_values_bam()
        pass

    def get_values_fastp(self):
        total_bases = self.fastp_json_file["before_filtering"]["total_bases"]
        total_fastp_bases = self.fastp_json_file["after_filtering"]["total_bases"]
        mean_read_length= self.fastp_json_file["after_filtering"]["read1_mean_length"]
        pass

    def get_values_hist(self):
        est_genome_size = self.hist_json_file["est_genome_size"]
        kmer_coverage_depth = self.hist_json_file["hom_peak"]["freq"]
        pass

    def get_values_bedtools(self):
        print("pp")
        pass

    def get_values_bam(self):
        print("pp")
        pass