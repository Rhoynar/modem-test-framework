
import subprocess

def run_cmd(cmd):
    cmd_obj = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return '\n'.join(cmd_obj.communicate())