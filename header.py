#######################################################################################
# header
#
# header.py
# Written by Evan Wilde
# April 6 2014
#
# Contains the heading information class
#######################################################################################

import re
import os
import time

file_name_pattern = "/([a-zA-Z0-9_-]*)\.([a-zA-Z0-9]*)$"
file_name_pattern = re.compile(file_name_pattern)

class header:
	"""Heading Data"""
	username = ""
	email = ""

	filepath = ""
	filecreatetime = None

	def __init__(self, username, email, filepath):
		self.username = username
		self.email = email
		self.filepath = filepath
		filecreatetime = time.ctime(os.path.getctime(filepath))

	def set_username(self, name):
		self.username = name

	def get_username(self):
		return self.username

	def set_email(self, email):
		self.email = email

	def get_email(self):
		return self.email

	def set_filedata(self, filepath):
		self.filepath = filepath

	def get_filepath(self):
		return self.filepath

	def get_filename(self):
		(filename, file_extension) = file_name_pattern.match(self.filepath).groups()
		return filename

	def get_file(self):
		(filename, file_extension) = file_name_pattern.match(self.filepath).groups()
		return filename + "." + file_extension

	def get_extension(self):
		(filename, file_extension) = file_name_pattern.match(self.filepath).groups()
		return file_extension
