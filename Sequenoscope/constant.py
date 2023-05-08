#!/usr/bin/env python

from dataclasses import dataclass

analyze_report_columns = ["Sample_id",
"Estimated genome size",
"Estimated kmer coverage depth",
"Total_bases",
"Total_fastp_bases",
"Mean Read length",
"Taxon id",
"Taxon_length",
"Taxon_covered_bases",
"Taxon_%_covered",
"Taxon_mean_read_len"
]

@dataclass(frozen=True)
class SequenceTypes:
    paired_end: str = 'PE'
    single_end: str = 'SE'

@dataclass(frozen=True)
class DefaultValues:
    minimap2_kmer_size: int = 15
    kat_hist_kmer_size: int = 27
    nanoget_threshold: int = 128
    samtools_idxstats_field_number: int = 4
    fastq_sample_row_number: int = 4
    fastq_line_starter: str = "@"