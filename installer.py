# Import scripts from the scripts folder to install all the config files
# Needs to be executed from this file path
import install_scripts.vscode as vscode
vscode.InstallConfig()

installation_functions = [
    ('vscode',vscode.InstallConfig),
]

for app in installation_functions:
    name = app[0]
    func = app[1]

    try:
        func()
        print(F'{name} Set up with no errors')
    except:
        print(F'ERROR setting up: {name}')