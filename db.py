# -*- coding: utf-8 -*-
import sys
# Workaround for autoconf bug. See https://github.com/priitj/whitedb/issues/25
sys.path.append("/usr/lib/python3.4/site-packages")
import whitedb
import wgdb
import pickle

class DB():

    def __init__(self):
        super(DB, self).__init__()
        self.db = whitedb.connect(local=1)
        self.db.set_locking(0)
        self.cursor = self.db.cursor()

    # _update_tag takes a string, a Record object, and an integer
    def _update_tag(self, tag, link, linkField):
        tagRec = self.db.insert(('tag', tag, link))
        link.set_field(linkField, tagRec)

    # TODO: Implement _dedup_tags
    def _dedup_tags():
        None

    # TODO: Implement _update_dump
    def _update_dump():
        None

    # create_note takes a string and a list of strings
    def create_note(self, data, tags):
        noteRec = self.db.create_record(len(tags) + 2)
        noteRec.set_field(0, 'note')
        noteRec.set_field(1, data)

        for i, tag in enumerate(tags, start=2):
            self._update_tag(tag, noteRec, i)

        return noteRec

    # display_note takes a Record object, and a integer
    def get_field(self, note, field):
        return (note.get_field(field))

    # update_note takes a Record object, a string, and a list of strings
    def update_note(self, note, data, tags):
        tmpTags = {}
        tags = set(tags)
        keySet = set()

        for i in range(2, note.get_size()):
            value = note.get_field(i)
            key = value.get_field(1)
            tmpTags.update({key: [value, i]})
            keySet.update([key])

        if len(keySet) == len(tags):
            if keySet == tags:
                note.set_field(1, data)

            else:
                note.set_field(1, data)
                addTags = tags - keySet
                rmTags = keySet - tags

                for i, tag in enumerate(rmTags):
                    self._update_tag(addTags[i], note, tmpTags[tag][1])

        else:
            updatedNote = self.create_note(data, tags)

            for i in keySet:
                tagLink = tmpTags[i][0]

                for j in range(2, tagLink.get_size()):
                        if tuple(tagLink[j])[1] == tuple(note)[1]:
                            tagLink.set_field(j, None)

            note.delete()
            return updatedNote

    # search_notes taks a string
    def search_notes(self, query):
        query = query.split(' ')
        result = set()

        for i in query:  # TODO: Search NOT foo.
            self.cursor.execute(arglist=[(0, wgdb.COND_EQUAL, 'tag'), (1, wgdb.COND_EQUAL, i)])

            for j in self.cursor.fetchall():
                tmp = list(j)
                del tmp[0:2]
                result.update(set(tmp)) if len(result) == 0 else result.update(set(tmp) & result)

        return list(result)

    def dump_db(self, filename):
        None

    def load_db(self, filename):
        None