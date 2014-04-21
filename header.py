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
	__username = ""
	__email = ""
	__file_data = None
	
	def __init__(self, username, email, filepath):
		"""Create a new header object"""
		self.__username = username
		self.__email = email

		self.__file_data = files.fileProperty(filepath)

	def get_username(self):
		"""Returns the name that will be applied to the source headers"""
		return self.__username

	def get_email(self):
		"""Returns the email of the current user"""
		return self.__email

	def get_filepath(self):
		"""Returns the absolute filepath"""
		return self.__file_data.get_filepath()

	def get_filename(self):
		"""Returns the filename without extension or path"""
		return self.__file_data.get_filename()

	def get_file(self):
		"""Returns the filename and extension"""
		return self.__file_data.get_file()

	def get_extension(self):
		"""Returns the extension of the file"""
		return self.__file_data.get_extension()

	def get_create_time(self):
		"""Returns the last modified time"""
		return self.__file_data.get_ctime()
	
	def __repr__(self):
		"""A pretty representation of the header data"""
		return "{0} <{1}>\nFilename: {2} -- {4}\nExtension: {3}".format(self.__username, self.__email, self.get_filename(), self.get_extension(), self.get_create_time())
