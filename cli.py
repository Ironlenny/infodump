# -*- coding: utf-8 -*-
import sys
import configparser
import control


class CLI():

    def __init__(self, filename='infodump.conf'):
        super(CLI, self).__init__()
        self.config = configparser.ConfigParser()
        try:
            self.config.read_file(open(filename))
            print(self.config['Database'])
        except configparser.MissingSectionHeaderError as err:
            print(err)
            sys.exit()
        self.control = control.Controller(self.config)
