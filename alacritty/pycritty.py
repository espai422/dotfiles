#!/bin/python
import argparse
import yaml
import os
from pathlib import Path

global PathPy
PathPy = __file__.split('/')
PathPy = '/'.join(PathPy[0:-1])


def DATA():
#obrir alavritty.yaml i transformar a diccionari
    path = str(Path.home())+'/.config/alacritty/alacritty.yml'
    with open (path,'r') as f:
        config = yaml.load(f , Loader=yaml.FullLoader)
    return config


def Themes(theme):
    if theme == None:
        return
    global config
    theme = PathPy+'/themes/'+theme+'.yaml'
#obrir tema i transformar en diccionari
    with open (theme,'r') as f:
        theme = yaml.load(f , Loader=yaml.FullLoader)

    config['colors']=theme['colors']

def get_fonts():
        with open (PathPy+'/fonts.yaml','r') as f:
            DC_fonts = yaml.load(f , Loader=yaml.FullLoader) 
        return DC_fonts

def font(font):
    if font == None:
        return
    global config
    fonts = get_fonts()
    endfont = fonts['fonts'][font]

    config['font']['bold']['family'] = endfont
    config['font']['italic']['family'] = endfont
    config['font']['normal']['family'] = endfont

def fontsize(size):
    if size == None:
        return
    global config
    config['font']['size'] = size


def opacity(val):
    if val == None:
        return
    global config
    config['background_opacity'] = val

def padding(val):
    if val == None:
        return
    global config
    config['window']['padding']['x']= val

def cursor(val):
    if val == None:
        return
    global config
    config['cursor']['style'] = val 

def cli():
    parser = argparse.ArgumentParser(
        prog= 'pycritty',
        description= 'python script to customize Alacritty',

    )
    parser.add_argument(
        '-o','--opacity',
        type= float,
        help= 'change font size',
    )
    parser.add_argument(
        '-t', '--theme',
        type= str,
        help= 'change themes (colors)',
    )
    parser.add_argument(
        '-f', '--font',
        type= str,
        help= 'change font',
    )
    parser.add_argument(
        '-s', '--fontsize',
        type= int,
        help= 'change fontsize',
    )
    parser.add_argument(
        '-c', '--cursor',
        type= str,
        help= 'change the terminal cursor',
    )
    parser.add_argument(
        '-p', '--padding',
        type= int,
        help= 'needs two arguments X and Y, sets padding',
    )
    return parser.parse_args()




if __name__ == '__main__':
    args = cli()
    config = DATA()

    Themes(args.theme)
    font(args.font)
    fontsize(args.fontsize)
    opacity(args.opacity)
    padding(args.padding)
    cursor(args.cursor)
    
    with open(str(Path.home())+'/.config/alacritty/alacritty.yml','w') as file:
        yaml.dump(config, file)
