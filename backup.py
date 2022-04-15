# This script need to be executed from it's path
# WORKING: vscode
# TODO: alacritty, Nerd Fonts, Qtile, rofi

import backup_scripts.vscode as vscode

backup_functions = [
    ('vscode',vscode.backup),
]

for app in backup_functions:
    name = app[0]
    func = app[1]

    try:
        func()
        print(F'{name} backup with no errors')
    except:
        print(F'Error creating the backup {name}')

