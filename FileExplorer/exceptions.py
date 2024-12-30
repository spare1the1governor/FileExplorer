'''Кастомные исключения'''


class FileNotFoundException(Exception):
    '''File doesn't exist'''
    pass
class CurrentDirectoryError(Exception):
    ''' Perhaps you( or someone else ) deleted something unnecessary from your computer '''
    pass

class FileNameFormatError(Exception):
     pass