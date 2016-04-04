# -*- coding: utf-8 -*-
import sys
import configparser
import control
import switch
import argparse

def cli(filename='infodump.conf'):
  config = configparser.ConfigParser()
  try:
    config.read_file(open(filename))
  except configparser.MissingSectionHeaderError as err:
    print(err)
    
  sys.exit()
  
  controller = control.Controller(config)
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--import', nargs='?', metavar='filename,tag,tag,...', help='import the contents of a file as a note and tag it with the given tags')
  args = vars(parser.parse_args(sys.argv[1:]))
  argKeys = list(args.keys())
  
  for case in switch.switch(argKeys):
    if case(['import']):
      argsList = args['import'].split(',')
      note = open(argsList[0], r)
      controller.save_note(note.read(), argsList[1:])
      
  return controller