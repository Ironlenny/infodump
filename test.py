import sys
from gui import Gui
from OpenGL import GL # Workaround for
                      # https://bugs.launchpad.net/ubuntu/+source/python-qt4/+bug/941826
import db


mainDB = db.DB()
mainDB.create_note('This is a note', ['note', 'programming', 'python', 'whitedb'])
notes = mainDB.search_notes('note programming')
print(notes)
for i in notes:
    print((mainDB.get_field(i, 1)))

mainDB.update_note(notes[0], 'This is a new and imporoved note', ['note', 'programming', 'python', 'whitedb'])

print((mainDB.get_field(notes[0], 1)))

notes = mainDB.update_note(notes[0], 'This note has one more tag', ['note', 'programming', 'python', 'whitedb', 'graph database'])

print((mainDB.get_field(notes, 1)))

mainDB.dump_db('foo')

#mainGui = Gui()
#mainGui.run()
sys.exit()