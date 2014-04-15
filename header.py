#######################################################################################
# header
#
# header.py
# Written by Evan Wilde
# April 6 2014
#
# Contains the heading information class
#######################################################################################
import files

class header:
	"""Heading Data Container"""
	username = ""
	email = ""
	file_data = None
	
	def __init__(self, username, email, filepath):
		"""Create a new header object"""
		self.username = username
		self.email = email

		self.file_data = files.fileProperty(filepath)

	def set_username(self, name):
		"""Sets the name that will be applied to the source headers -- Might be deprecated soon"""
		self.username = name

	def get_username(self):
		"""Returns the name that will be applied to the source headers"""
		return self.username

	def set_email(self, email):
		"""Sets an email for a user --- Might become deprecated soon"""
		self.email = email

	def get_email(self):
		"""Returns the email of the current user"""
		return self.email

	def get_filepath(self):
		"""Returns the absolute filepath"""
		return self.file_data.get_filepath()

	def get_filename(self):
		"""Returns the filename without extension or path"""
		return self.file_data.get_filename()

	def get_file(self):
		"""Returns the filename and extension"""
		return self.file_data.get_file()

	def get_extension(self):
		"""Returns the extension of the file"""
		return self.file_data.get_extension()

	def get_create_time(self):
		"""Returns the last modified time"""
		return self.file_data.get_ctime()
	
	def __repr__(self):
		"""A pretty representation of the header data"""
		return "{0} <{1}>\nFilename: {2} -- {4}\nExtension: {3}".format(self.username, self.email, self.get_filename(), self.get_extension(), self.get_create_time())
