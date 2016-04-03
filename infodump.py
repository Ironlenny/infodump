# -*- coding: utf-8 -*-
import sys
import cli

# Workaround for
# https://bugs.launchpad.net/ubuntu/+source/python-qt4/+bug/941826
from OpenGL import GL

def main():
    mainCLI = cli.CLI()


main()