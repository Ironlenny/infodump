# -*- coding: utf-8 -*-
import sys
import configparser
sys.path.append("../core/")
import control
#import switch
import argparse

def cli(filename='infodump.conf'):
    config = configparser.ConfigParser()
    try:
        config.read_file(open(filename))
    except configparser.MissingSectionHeaderError as err:
        print(err)

    controller = control.Controller(config)
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--import', nargs='?', metavar='filename,tag,tag,...',
                      help='import the contents of a file as a note and tag it with the given tags')
    parser.add_argument('-s', '--search', nargs='?', metavar='tag,tag,...',
                      help='search database for note matching the given tags')

    if len(sys.argv) != 1:
        args = vars(parser.parse_args(sys.argv[1:]))
        argKeys = list(args.keys())

    if args['import'] != None:
        argsList = args['import'].split(',')
        note = open(argsList[0], 'r')
        controller.save_note(note.read(), argsList[1:])
    elif args['search'] != None:
        argsList = args['search']
        print(controller.search(argsList))
    else:
        print("Error: no or incorrect argument given")

    return controller