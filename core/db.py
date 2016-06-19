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
# TODO: Conditional import of different dedupe algos
# TODO: Conditional import of different search algos


class DB():

    def __init__(self, filename, locking, local):
        super(DB, self).__init__()
        self.db = whitedb.connect(local=local)  # Connect to db, use only local mem
        self.db.set_locking(locking)  # Disable lock, perf boost for single user
        self.cursor = self.db.cursor()
        self.recCount = 0
        # Serialization aids, metadata, data
        # TODO: Change 'meta' to 0 and 'id' to 1, so notes and tags share the same structure.
        self.Field = enum.Enum('Field', {'id': 0, 'time': 1, 'meta': 2, 'data': 3, 'tags': 4, 'tagName': 1})
        self.dbFile = shelve.open(filename)

    # TODO: Move all expections here
    def _test_type(self, obj):
        return

    # _update_tag takes a string, a Record object, and an integer
    # TODO: Write to take only dict. Incorporate for loop from _create_note()
    def _update_tag(self, tag, link, linkField):
        tagRec = self.db.insert(('tag', tag, link))
        link.set_field(linkField, tagRec)

    # TODO: Make updates transactional
    def _update_disk(self, recID, recTime, recMeta, recData, recTags):
        self.dbFile[str(recID)] = (recTime, recMeta, recData, recTags)

    # TODO: Implement _dedupe_tags
    def dedupe_tags(self):
        self.delete_record()
        return

    def delete_record(self):
        return

    def _create_note(self, meta, data, tags, recID, recTime):
        if not isinstance(data, str):
            raise TypeError('TypeError: data is not a string')
        elif not isinstance(tags, list) or not all(isinstance(item, str) for item in tags):
            raise TypeError('TypeError: tags is not at list of strings')

        noteRec = self.db.create_record(len(tags) + self.Field.tags.value)
        noteRec.set_field(self.Field.id.value, recID)
        noteRec.set_field(self.Field.time.value, recTime)
        noteRec.set_field(self.Field.meta.value, meta)
        noteRec.set_field(self.Field.data.value, data)

        for i, tag in enumerate(tags, start=self.Field.tags.value):
            self._update_tag(tag, noteRec, i)

        return noteRec

    # create_note takes a string and a list of strings
    def create_note(self, data, tags):
        recTime = time.time()
        meta = 'note'
        self._update_disk(self.recCount, recTime, meta, data, tags)
        note = self._create_note(meta, data, tags, self.recCount, recTime)
        self.recCount += 1
        return note

    # display_note takes a Record object, and a integer
    def get_field(self, record, field):
        return (record.get_field(field))

    # update_note takes a Record object, a string, and a list of strings
    def update_note(self, note, data, tags):
        if not isinstance(data, str):
            raise TypeError('TypeError: data is not a string')
        elif not isinstance(tags, list) or not all(isinstance(item, str) for item in tags):
            raise TypeError('TypeError: tags is not at list of strings')

        tmpTags = {}
        tags = set(tags)
        keySet = set()
        dataField = self.Field.data.value

        # Make dict of tag names and link records
        for i in range(self.Field.tags.value, note.get_size()):
            value = note.get_field(i)  # Get tag record
            key = value.get_field(1)  # Get name of tag
            # Set tag name, link, and postion in note record
            tmpTags.update({key: [value, i]})
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

                # TODO: Move loop into _update_tag()
                for i, tag in enumerate(rmTags):
                    self._update_tag(addTags[i], note, tmpTags[tag][1])

        # If update bigger than current. Create new, update links, delete old
        else:
            recTime = time.time()
            self._update_disk(note.get_field(recID), recTime, note.get_field(meta), data, tags)
            updatedNote = self._create_note(note.get_field(meta), data, list(tags), note.get_field(recID), recTime)

            for i in keySet:
                tagLink = tmpTags[i][0]  # Get link record

                # TODO: Move loop to _update_tag()
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
            self._create_note(recTuple[1], recTuple[2], list(recTuple[3]), i, recTuple[0])

        self.dedupe_tags()

    def get_enum(self, fieldType):
        value = self.Field[fieldType].value
        return value

    def get_tags(self, note):
        if not isinstance(note, whitedb.Record):
            raise TypeError('TypeError: note is not a whitedb.Record object')

        tags = []

        for i in range(self.Field.tags.value, len(tuple(note))):
            tag = note.get_field(i)
            tags.append(tuple(tag)[self.Field.tagName.value])

        return tags