# This module is copied from http://code.activestate.com/recipes/410692/
# It was written by Brian Beck and is licensed under Python Software
# Foundation license. A copy of the license is included with the source
# of this module.
class switch(object):
    def __init__(self, value):
        print('In switch class')
        self.value = value
        print(self.value)
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False