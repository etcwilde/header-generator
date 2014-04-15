#######################################################################################
# files
#
# files.py
# Written by Evan Wilde
# April 8 2014
#
# Gives a simple interface for getting properties on a file 
#######################################################################################

import re
import os
import time

# File Property
#
# An object capable of returning contents of a file
# 
class fileProperty(object):
	"""docstring for fileProperty"""
	filepath = ""
	filecreatetime = None
	file_name_pattern = re.compile("^.*/(.*)\.(.*)$")

	def __init__(self, filepath):
		"""Creates a new file property"""
		self.filepath = os.path.abspath(filepath)
		self.filecreatetime = time.ctime(os.path.getctime(filepath))

	def __eq__(self, other):
		"""Determines if two files are the same"""
		return self.get_filepath() == other.get_filepath()

	def __hash__(self):
		"""Hashing function for fileproperties
			This is the result of the python string hash function on the filepath"""
		return hash(self.filepath)


	def open(self, mode = 'r', buffering = -1, encoding = None, errors = None, newline = None, closefd = True, opener = None):
		"""Returns an opened file"""
		try:
			return open(self.filepath, mode, buffering, encoding, errors, newline, closefd, opener)
		except Exception:
			print ("Could not open file: %s" % self.filepath)
			return None

	def get_lines(self):
		f = self.open()
		if f:
			for line in f:
				yield line
			f.close()
		else:
			return ""


	def get_filepath(self):
		"""Returns the absolute filepath"""
		return self.filepath

	def get_filename(self):
		"""Returns the filename without extension or path"""
		(filename, _) = self.file_name_pattern.match(self.filepath).groups()
		return filename

	def get_file(self):
		"""Returns the filename and extension"""
		try:
			(filename, file_extension) = self.file_name_pattern.match(self.filepath).groups()
		except AttributeError:
			print ("No file extension!")


		return filename + "." + file_extension

	def get_extension(self):
		"""Returns the extension of the file"""
		try:
			(_, file_extension) = self.file_name_pattern.match(self.filepath).groups()
		except AttributeError:
			print ("No file extension")
		return file_extension

	def get_ctime(self):
		"""Returns last modified time of a file"""
		return self.filecreatetime

	def set_file_pattern(self, pattern):
		"""Sets the file search pattern for, allowing for different file patterns
		If the pattern is unable to compile, it will revert to the previous pattern"""
		old_pattern = self.file_name_pattern
		try:
			new_pattern = re.compile(pattern)
		except Exception:
			print ("Error: Pattern Could Not Be Compiled")
			new_pattern = old_pattern
		self.file_name_pattern = new_pattern

	def __str__(self):
		"""String representation of the file data"""
		return str(self.get_file())

	def __repr__(self):
		"""A pretty representation of the file data"""
		return str(self.get_file())

		
