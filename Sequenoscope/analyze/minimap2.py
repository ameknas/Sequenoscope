from analyze import run_command

Input = "seq1.fastq"
ref = "ref.fasta"
class Illumina_Sequencing_data: 
    def __init__(self, fastq_file, ref_file):
        self.fastq_file = fastq_file
        self.ref_file = ref_file
        pass

    def align(self):
        minimap_align_command = "minimap2 -ax sr {} {} > output.sam".format(self.ref_file, self.fastq_file)
        run_command(minimap_align_command)

    def sort(self):
        samtools_sort = "samtools view -S -b -F 4 output.sam | samtools sort -T 15 --reference {} -o mapped.bam".format(self.ref_file)
        run_command(samtools_sort)

Illumina_Sequencing_data(Input,ref)
Illumina_Sequencing_data.align()
Illumina_Sequencing_data.sort()

class ONT_Sequencing_Data:
    pass

class PacificBio_Sequencing_Data:
    pass