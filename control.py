# -*- coding: utf-8 -*-
import db
import logger


class Controller():

    def __init__(self, filename='infodump.db', locking=0, local=1):
        super(Controller, self).__init__()
        self.info = db.DB(filename, locking, local)

    def _split_tags(self, tags):
        return tags.lower().split(', ')

    def save_note(self, text, tags):
        if tags is not str:
            raise TypeError ('TypeError: tags is not a string')

        tags = self._split_tags(tags)
        try:
            return self.info.create_note(text, tags)
        except TypeError as err:
            logger.log(err, 'err')

    def search(self, query):
        result = {}
        query = self.info.search_notes(query)
        for i in query:
            try:
                result.update({tuple(i)[self.info.get_enum('data')]: self.info.get_tags(i)})
            except TypeError as err:
                logger.log(err, 'err')

        return result

    def update_note(self, note, data, tags):
        tags = self._split_tags(tags)
        try:
            return self.info.update_note(note, data, tags)
        except TypeError as err:
            logger.log(err, 'err')

    def delete_note(self, note):
        return