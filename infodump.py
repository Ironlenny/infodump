# -*- coding: utf-8 -*-
import sys
import cli
import gui

# Workaround for
# https://bugs.launchpad.net/ubuntu/+source/python-qt4/+bug/941826
from OpenGL import GL

controller = cli.cli()

app = gui.Gui(controller)

sys.exit(app.run())