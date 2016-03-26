# -*- coding: utf-8 -*-
import sys
# Workaround for autoconf bug. See https://github.com/priitj/whitedb/issues/25
sys.path.append("/usr/lib/python3.4/site-packages")
import whitedb
import wgdb
# TODO: Better on disk format. A key/value store is not ideal for representing
# a graph structure. Maybe FlatBuffers?
import shelve
import time
import enum

class DB():

    def __init__(self, filename='infodump.db', locking=0, local=1):
        super(DB, self).__init__()
        self.db = whitedb.connect(local=local)  # Connect to db, use only local mem
        self.db.set_locking(locking)  # Disable lock, perf boost for single user
        self.cursor = self.db.cursor()
        self.recCount = 0
        # Serialization aids, metadata, data
        self.Field = enum.Enum('Field', {'id': 0, 'time': 1, 'meta': 2, 'data': 3})
        self.fieldOffset = len(self.Field)
        self.dbFile = shelve.open(filename)

    # _update_tag takes a string, a Record object, and an integer
    def _update_tag(self, tag, link, linkField):
        tagRec = self.db.insert(('tag', tag, link))
        link.set_field(linkField, tagRec)

    # TODO: Implement _dedup_tags
    def _dedup_tags():
        return

    # TODO: Make updates transactional
    def _update_disk(self, recID, recTime, recMeta, recData, recTags):
        self.dbFile[str(recID)] = (recTime, recMeta, recData, recTags)

    # create_note takes a string and a list of strings
    def _create_note(self, meta, data, tags, recID, recTime):

        noteRec = self.db.create_record(len(tags) + self.fieldOffset)
        noteRec.set_field(self.Field.id.value, recID)
        noteRec.set_field(self.Field.time.value, recTime)
        noteRec.set_field(self.Field.meta.value, meta)
        noteRec.set_field(self.Field.data.value, data)

        for i, tag in enumerate(tags, start=self.fieldOffset):
            self._update_tag(tag, noteRec, i)

        return noteRec

    def create_note(self, data, tags):
        recTime = time.time()
        meta = 'note'
        self._update_disk(self.recCount, recTime, meta, data, tags)
        self._create_note(meta, data, tags, self.recCount, recTime)
        self.recCount += 1

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
            recID = self.Field.id.value
            meta = self.Field.meta.value

        if len(keySet) == len(tags):
            if keySet == tags:
                note.set_field(dataField, data)

            # Find set of tags added and set of tags removed. Update note record.
            else:
                note.set_field(dataField, data, True)
                addTags = tags - keySet
                rmTags = keySet - tags
                recTime = self.Field.time.value
                self._update_disk(note.get_field(recID), note.get_field(recTime), note.get_field(meta), data, tags)

                for i, tag in enumerate(rmTags):
                    self._update_tag(addTags[i], note, tmpTags[tag][1])

        # If update bigger than current. Create new, update links, delete old
        else:
            recTime = time.time()
            self._update_disk(note.get_field(recID), recTime, note.get_field(meta), data, tags)
            updatedNote = self._create_note(note.get_field(meta), data, tags, note.get_field(recID), recTime)

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
        # TODO : Wildcard search
        # TODO: NOT search
        # TODO: String search
        for i in query:
            self.cursor.execute(arglist=[(0, wgdb.COND_EQUAL, 'tag'), (1, wgdb.COND_EQUAL, i)])

            for j in self.cursor.fetchall():
                tmp = list(j)
                del tmp[0:2]
                result.update(set(tmp)) if len(result) == 0 else result.update(set(tmp) & result)

        return tuple(result)

    def load_db(self):

        for i in list(self.dbFile.keys()):
            recTuple = tuple(self.dbFile[i])
            self._create_note(recTuple[1], recTuple[2], recTuple[3], i, recTuple[0])

