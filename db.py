# -*- coding: utf-8 -*-
import sys
# Workaround for autoconf bug. See https://github.com/priitj/whitedb/issues/25
sys.path.append("/usr/lib/python3.4/site-packages")
import whitedb
import wgdb
import pickle
import time
import datetime
import enum

class DB():

    def __init__(self, filename='infodump.db'):
        super(DB, self).__init__()
        self.db = whitedb.connect(local=1)  # Connect to db, use only local mem
        self.db.set_locking(0)  # Disable lock, perf boost for single user
        self.cursor = self.db.cursor()
        self.recCount = 0
        # Serialization aids, metadata, data
        self.Field = enum.Enum('Field', {'id': 0, 'date': 1, 'time': 2, 'meta': 3, 'data': 4})
        self.fieldOffset = len(self.Field)

    # _update_tag takes a string, a Record object, and an integer
    def _update_tag(self, tag, link, linkField):
        tagRec = self.db.insert(('tag', tag, link))
        link.set_field(linkField, tagRec)

    # TODO: Implement _dedup_tags
    def _dedup_tags():
        None

    # TODO: Implement _update_disk
    def _update_disk(recTuple):
        None

    # create_note takes a string and a list of strings
    def create_note(self, data, tags, _id=None, _noIncrement=False):

        idField = self.Field.id.value
        dateField = self.Field.date.value
        timeField = self.Field.time.value
        metaField = self.Field.meta.value
        fieldData = self.Field.data.value
        date = datetime.date.today()
        recTime = time.time()
        recID = self.recCount if _noIncrement is False else _id
        noteRec = self.db.create_record(len(tags) + self.fieldOffset)

        noteRec.set_field(idField, recID)
        noteRec.set_field(dateField, date)
        noteRec.set_field(timeField, recTime)
        noteRec.set_field(metaField, 'note')
        noteRec.set_field(fieldData, data)



        if _noIncrement is False:
            self.recCount += 1

        for i, tag in enumerate(tags, start=self.fieldOffset):
            self._update_tag(tag, noteRec, i)

        return noteRec

    # display_note takes a Record object, and a integer
    def get_field(self, record, field):
        return (record.get_field(field))

    # update_note takes a Record object, a string, and a list of strings
    def update_note(self, note, data, tags):
        tmpTags = {}
        tags = set(tags)
        keySet = set()
        dataField = self.Field.data.value

        # Make dict of tag names and link records
        for i in range(self.fieldOffset, note.get_size()):
            value = note.get_field(i)  # Get tag record
            key = value.get_field(1)  # Get name of tag
            tmpTags.update({key: [value, i]})  # Set tag name, link, and postion in note record
            keySet.update([key])

        if len(keySet) == len(tags):
            if keySet == tags:
                note.set_field(dataField, data)

            # Find set of tags added and set of tags removed. Update note record.
            else:
                note.set_field(dataField, data, True)
                addTags = tags - keySet
                rmTags = keySet - tags

                for i, tag in enumerate(rmTags):
                    self._update_tag(addTags[i], note, tmpTags[tag][1])

        # If update bigger than current. Create new, update links, delete old
        else:
            updatedNote = self.create_note(data, tags, note.get_field(self.Field.id.value), True)

            for i in keySet:
                tagLink = tmpTags[i][0]  # Get link record

                # For each link in tag record, compare with note data. If match,
                # replace with None.
                for j in range(2, tagLink.get_size()):
                        if tuple(tagLink[j])[dataField] == tuple(note)[dataField]:
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

        return tuple(result)


    def load_db(self, filename):
        None