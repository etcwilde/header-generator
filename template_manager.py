#######################################################################################
# Template manager
#
# template_manager.py
# Written by Evan Wilde
# April 16 2014
# 
# Manges installed license templates and imports new ones. 
#######################################################################################
import files
import header
import os
import pickle
import re
import sys

#################
# Regex patterns
#################
#--[Input File Patterns] ----------------------------
hidden_file_pattern = "^\.(.*)"
file_name_pattern = "^([a-zA-Z0-9_-]*)\.([a-zA-Z0-9]*)$"
hidden_file_pattern = re.compile(hidden_file_pattern)
file_name_pattern = re.compile(file_name_pattern)

#--[Template File Patterns] -------------------------
Template_Start_pattern = "---START"
Template_End_pattern = "---END"
Template_Type_pattern = "^TYPE:(.*)"
Template_Include_pattern = "^INCTYPE:(.*)"

Template_Type_pattern = re.compile(Template_Type_pattern)
Template_Include_pattern = re.compile(Template_Include_pattern)


def list_dir_visible(path):
	for f in os.listdir(path):
		if not f.startswith('.'):
			yield f

# Template
#
# Templates contains information on individual template files.
# This will include the metadata and the contents of the template.
class Template:
	"""Contains the metadata for a template file
		The template is a hashable Object
	"""

	def __init__(self, template_filename):
		"""Initializes a template file"""
		self.include_pattern = ""
		self.type_associations = []
		self.template_file = files.fileProperty(template_filename)



		self.template_string = ""

		self.include_pos = False # if include position is false, include statements come after the header
		self.parse_template_file()

	def  __eq__(self, other):
		"""
		Template equality is defined by the file path
		TODO: Include file association in equality -- Maybe
		"""
		return self.get_file() == other.get_file()

	def __hash__(self):
		"""
		Hashing function for Templates
		Uses the hashing function for fileProperty
		"""

		return hash(self.get_file())

	def __repr__(self):
		"""
		Human readable representation of a template
		"""
		return_string = self.template_file.get_file()
		#	if len(self.type_associations) > 0:
		#		return_string += ": "
		#		return_string += self.type_associations[0]
		#		for assoc in self.type_associations[1:]:
		#			return_string += ", " + assoc
		return return_string

	def __iter__(self):
		"""
		Iterates through the lines of the template file
		"""
		for line in self.template_file:
			yield line

	def parse_template_file(self):
		"""
		Reads the contents of the template file and fills members of the class
		"""
		intemplate = False
		done_template = False
		
		line_number = 0

		for line in self.template_file:
			line_number += 1
			
			if "--START" in line:
				intemplate = True
			elif "--END" in line and intemplate:
				intemplate = False
				done_template = True
			elif "--END" in line and not intemplate:
				print ("Syntax Error: {0}:{1} -- In Template".format(self.template_file, line_number))
			elif "<INC>" in line and not done_template:
				self.include_pos = True
			elif "INCTYPE" in line:
				try:
					(self.include_pattern,) = Template_Include_pattern.match(line).groups()
				except AttributeError:
					print ("Syntax Error: {0}:{1} -- Include Type".format(self.template_file, line_number))
			elif "TYPE" in line:
				try:
					(type_assoc,) = Template_Type_pattern.match(line).groups()
					self.type_associations.append(type_assoc)
				except AttributeError:
					pass

	def is_include_top(self):
		"""
		Returns true if include statements are before header
		"""
		return self.include_pos

	def get_include(self):
		"""
		Returns the include pattern
		i.e #include for c, import for python, etc...
		"""
		return self.include_pattern

	def update_associations(self):
		"""Unimplemented
		Updates the metadata headers for the template
		-- Deprecated, just use parse_template_file
		"""
		pass

	def get_associations(self):
		"""
		Returns the list of associated file types
		"""
		return self.type_associations

	def get_file(self):
		"""Returns the fileProperty of the Template"""
		return self.template_file

	def generate_header(self, header):
		"""
		Returns a string form of the header with all the lables filled out
		"""
		out_string = ""
		intemplate = False
		for line in self:
			if "--END" in line:
				intemplate = False
			elif intemplate:
				if "<FILE>" in line:
					line = line.replace("<FILE>", header.get_filename())
				if "<FILEPATH>" in line:
					line = line.replace("<FILEPATH>", header.get_filepath())
				if "<FILENAME>" in line:
					line = line.replace("<FILENAME>", header.get_file())
				if "<USERNAME>" in line:
					line = line.replace("<USERNAME>", header.get_username())
				if "<EMAIL>" in line:
					line = line.replace("<EMAIL>", header.get_email())
				if "<DATE>" in line:
					line = line.replace("<DATE>", header.get_create_time())
				out_string += line + "\n"
			elif "--START" in line:
				intemplate = True
		return out_string




# Template Manager
#
# Maintains the database of all the templates
class Template_manager:
	"""Template manager maintains the database of the installed templates and associated file extensions."""

	__filetype_registry = {}
	__registered_templates = []
	__template_location = ""
	__registry_updated = False

	def __init__(self, template_file_location):
		"""Initializes the template manager and database"""
		self.__template_location = template_file_location
		self.load_registry_file()

	def get_registered_files(self):
		"""Returns a list of registered fileProperty objects"""
		return [f.get_file() for f in self.__registered_templates]

	def get_registered_templates(self):
		"""Returns a list of registered Template objects"""
		return [f for f in self.__registered_templates]

	def get_template_metadata(self, template_filename):
		"""
		Reads the template metadata
		"""
		# print ("DEBUG > getting template metadata")
		t = Template(self.__template_location + "/" + template_filename)
		if t.get_file().exists():
			self.__registered_templates.append(t)

			# print ("DEBUG > getting template metadata")

			for line in t.get_file():
				file_ext = Template_Type_pattern.match(line)
				if file_ext:
					(file_ext,) = file_ext.groups()
					self.__filetype_registry[file_ext] = t

	def get_new_templates(self):
		"""
		Returns a list of unique templates that have been put in the template file
		but not registered with the database.
		"""
		directory_files = []
		dir_files = list_dir_visible(self.__template_location)
		for fname in dir_files:
			directory_files.append(files.fileProperty(self.__template_location + "/" + fname))
		return list(set(directory_files) - set(self.get_registered_files()))

	def get_removed_templates(self):
		"""
		Returns a list of unique templates that have been removed from the template file
		but not removed from the database
		"""
		directory_templates = []
		#print("DEBUG > ", self.__template_location)
		dir_files = list_dir_visible(self.__template_location)
		for fname in dir_files:

			directory_templates.append(Template(self.__template_location + "/" + fname))
		return list(set(self.get_registered_templates()) - set(directory_templates))

	def get_modified_templates(self):
		"""Unimplemented
		Returns a list of unique templates that have been modified, since their last update in the registry
		"""
		directory_files = []
		dir_files = list_dir_visible(self.__template_location)

		updated_files = []
		for f in directory_files:
			for f2 in self.get_registered_files():
				print("Directory File: {0} -- {1}\t Registry File: {2} -- {3}".format(f.get_file(), f.get_ctime(), f2.get_file(), f.get_ctime()))
				if (f.get_filepath() == f2.get_filepath()):
					print ("Same Kind")
				if (f == f2) and (f.get_ctime != f2.get_ctime):
					updated_files.append(f2)
		return updated_files

	def add_new_templates(self):
		"""Unimplemented
		Registers all new templates with the registry
		"""
		for new_template in self.get_new_templates():
			self.get_template_metadata(new_template.get_file())

	def remove_deleted_templates(self):
		"""Unimplemented
		Removes deleted registered templates from the registry
		"""
		for  removed_template in self.get_removed_templates():
			if removed_template in self.__registered_templates:
				self.__registered_templates.remove(removed_template)
			for assoc in removed_template.get_associations():
				#print ("Associated To:", assoc)
				del self.__filetype_registry[assoc]

	def update_modified_templates(self):
		"""Unimplemented
		Updates modified templates in the registry
		"""
		#print("Modified Templates:", self.get_modified_templates())
		pass

	def create_registry_file(self):
		"""
		Creates a new template registry database
		"""
		for template_file in list_dir_visible(self.__template_location):
			self.get_template_metadata(template_file)
		self.write_registry_file()

	def update_registry_file(self):
		"""Unimplemented
		Updates the template registry database
		Inserts new registry templates
		Removes deleted registry templates
		Updates modified registry templates
		"""
		self.add_new_templates()
		self.remove_deleted_templates()
		self.update_modified_templates()
		self.write_registry_file()

	def load_registry_file(self):
		"""
		Loads the contents of the registry into the class members
		"""
		registry_location = self.__template_location + "/.file_types.db"
		try:
			contains_registry = ".file_types.db" in os.listdir(self.__template_location)
			#print ("DEBUG > Registry exists:", contains_registry)
		except FileNotFoundError:
			print ("Error: Template Folder Not Found")
			exit()

		if not contains_registry:
			#print ("DEBUG > Create Registry")
			self.create_registry_file()
		else: # Don't update the registry here, instead we will run the updates when a template is not in our database
			#print ("DEBUG > Load Registry")
			registry_contents = pickle.load(open(registry_location, "rb"))
			self.__registered_templates = registry_contents[0]
			self.__filetype_registry = registry_contents[1]

	def search_templates(self, file_extension):
		"""Finds the corresponding template file for a given extension"""
		try:
			t = self.__filetype_registry[file_extension]
			if t.get_file().exists():
				return t
			else:
				self.update_registry_file()
				self.__registry_updated = True
		except KeyError:
			if not self.__registry_updated:
				self.update_registry_file()
				self.__registry_updated = True
			else:
				return None
			try:			
				return self.__filetype_registry[file_extension]
			except KeyError:
				return None

	def write_registry_file(self):
		"""Writes registered templates to the registry"""
		registry_location = self.__template_location + "/.file_types.db"
		lst = []
		lst.append(self.__registered_templates)
		lst.append(self.__filetype_registry)
		registry_file = open(registry_location, "wb")
		pickle.dump(lst, registry_file)
		registry_file.close()

