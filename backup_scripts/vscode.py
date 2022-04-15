import json
import subprocess
from pathlib import Path

PATH = F'{str(Path.home())}/.config/Code/User/extensions.json'

def backup():

    command = 'code --list-extensions'
    stdoutdata = subprocess.check_output(command, shell=True).decode('utf-8')

    extensions = stdoutdata.split('\n')
    extensions.remove("")

    with open(PATH, 'w') as f:
        f.write(json.dumps(extensions))