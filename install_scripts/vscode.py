# This script install all the dependences for vscode
# Then move the json file with the dependences installed in the .config/Code/user

import subprocess
import json
from pathlib import Path

PATH = './Code/User/'
VSCODE_CONFIG_PATH = F'{str(Path.home())}/.config/Code/User/'
#VSCODE_CONFIG_PATH = F'{str(Path.home())}/Proves'

FILES = ['settings.json', 'keybindings.json', 'extensions.json']

def get_extensions():

    extensions_path = F'{PATH}/{FILES[2]}'
    with open(extensions_path,'r') as f:
        extensions = json.loads(f.read())
    
    return extensions

def install_extensions(extensions: list):

    for extension in extensions:
        subprocess.run(['code','--install-extension', extension])

def InstallConfig():

    # Install extensions

    extensions = get_extensions()
    install_extensions(extensions)

    # Copy config files

    for file in FILES:
        src_path = F'{PATH}/{file}'
        dest_path = F'{VSCODE_CONFIG_PATH}/{file}'        
        subprocess.run(['cp', src_path, dest_path]) 

