##############################################################################
# files
#
# files.py
# Written by Evan Wilde
# April 8 2014
#
# Gives a simple interface for getting properties on a file
###############################################################################

import re
import os
import time


# File Property
#
# An object capable of returning contents of a file
#
class fileProperty:
    """docstring for fileProperty"""

    __file_name_pattern = re.compile("^.*/(.*)\.(.*)$")

    def __init__(self, filepath):
        """Creates a new file property"""
        self.__filepath = ""
        self.__filecreatetime = None
        self.__filepath = os.path.abspath(filepath)
        try:
            self.__filecreatetime = time.strftime("%b %d %Y",
                                                  time.localtime(
                                                      os.path.getctime(filepath)
                                                  )
                                                  )
        except Exception:
            pass

    def __eq__(self, other):
        """
        Determines if two files are the same
        Files are equal if the absolute filepath is the same.
        """
        return self.get_filepath() == other.get_filepath()

    def __hash__(self):
        """Hashing function for fileproperties
        This is the result of the python string hash function on the filepath"""
        return hash(self.__filepath)

    def __iter__(self):
        """Iterates through each line of the file"""
        f = self.open()
        if f:
            for line in f:
                yield line.strip('\n\r')
            f.close()
        else:
            yield ""

    def exists(self):
        """Returns if the file exists and is accessible"""
        try:
            f = open(self.__filepath)
            f.close()
            return True
        except IOError:
            return False

    def open(self, mode='r', buffering=-1, encoding=None, errors=None,
             newline=None, closefd=True, opener=None):
        """Returns an opened file"""
        try:
            return open(self.__filepath, mode, buffering, encoding, errors,
                        newline, closefd, opener)
        except IOError:
            print ("Could not open file: %s" % self.__filepath)
            return None

    def get_lines(self):
        """returns all the lines in the file"""
        f = self.open()
        if f:
            for line in f:

                yield str.strip(line)
            f.close()
        else:
            yield ""

    def get_filepath(self):
        """Returns the absolute filepath"""
        return self.__filepath

    def get_filename(self):
        """Returns the filename without extension or path"""
        (filename, _) = self.__file_name_pattern.match(self.__filepath).groups()
        return filename

    def get_file(self):
        """Returns the filename and extension"""
        try:
            (filename, file_extension) = self.__file_name_pattern.match(
                self.__filepath).groups()
        except AttributeError:
            print ("No file extension!")
        return filename + "." + file_extension

    def get_extension(self):
        """Returns the extension of the file"""
        try:
            (_, file_extension) = self.__file_name_pattern.match(
                self.__filepath).groups()
        except AttributeError:
            print ("No file extension")
        return file_extension

    def get_ctime(self):
        """Returns last modified time of a file"""
        return self.__filecreatetime

    def set_file_pattern(self, pattern):
        """Sets the file search pattern for, allowing for different file patterns.
        If the pattern is unable to compile, it will revert to the previous
        pattern."""
        old_pattern = self.__file_name_pattern
        try:
            new_pattern = re.compile(pattern)
        except Exception:
            print ("Error: Pattern Could Not Be Compiled")
            new_pattern = old_pattern
        self.__file_name_pattern = new_pattern

    def __str__(self):
        """String representation of the file data"""
        return str(self.get_file())

    def __repr__(self):
        """A pretty representation of the file data"""
        return str(self.get_file())
