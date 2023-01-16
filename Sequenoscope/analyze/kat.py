from analyze import run_command

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



