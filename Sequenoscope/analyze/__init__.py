from subprocess import Popen, PIPE

def run_command(command):
    p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    return stdout, stderr

class Sequence:
    technology = None
    files = []
    is_paired = False
    out_files = ''

    def __init__(self, tech_name, list_of_seq):
        self.technology = tech_name
        self.files = list_of_seq
        self.classify_seq()
        return

    def classify_seq(self):
        if len(self.files) == 2:
            is_paired = True

    def is_string(self,input):
        #do something
        return isinstance(input,str)

    def output_formatted_files(self):
        self.out_files = " ".join(self.files)


