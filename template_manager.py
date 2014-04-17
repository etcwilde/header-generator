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
		self.template_file = None
		self.include_pattern = ""
		self.type_associations = []
		self.template_file = files.fileProperty(template_filename)

		line_number = 0
		for line in self.template_file:
			line_number += 1
			if Template_Start_pattern in line:
				break
			if Template_End_pattern in line:
				print ("Syntax Error: File {0}, No template beginning".format(self.template_file.get_filepath()))

			# Parser parts
			if "INCTYPE" in line:
				try:
					(self.include_pattern,) = Template_Include_pattern.match(line).groups()
					print
				except AttributeError:
					print ("error doing a thing")

			if "TYPE" in line:
				try:
					(type_assoc,) = Template_Type_pattern.match(line).groups()
					self.type_associations.append(type_assoc)

				except AttributeError:
					pass
					#print ("Syntax Error: File {0}, Undefined file association: {1}".format(self.template_file.get_filepath(), line_number))

	def  __eq__(self, other):
		"""
		Template equality is defined by the file path
		TODO: Include file association in equality
		"""
		return self.get_file() == other.get_file()

	def __hash__(self):
		"""
		Hashing function for Templates
		Uses the hashing function for fileProperty
		"""

		return hash(self.get_file())

	def __repr__(self):
		return_string = self.template_file.get_file()
	#	if len(self.type_associations) > 0:
	#		return_string += ": "
	#		return_string += self.type_associations[0]
	#		for assoc in self.type_associations[1:]:
	#			return_string += ", " + assoc
		return return_string

	def update_associations(self):
		"""Unimplemented
		Updates the metadata headers for the template
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
		t = Template(self.__template_location + "/" + template_filename)
		if t.get_file().exists():
			self.__registered_templates.append(t)
			for line in t.get_file():
				file_ext = Template_Type_pattern.match(line)
				if file_ext:
					(file_ext,) = file_ext.groups()
					self.__filetype_registry[file_ext] = t
		#try:
		#	f = files.fileProperty(self.__template_location + "/" + template_filename)
		#	for line in f:
		#		file_ext = Template_Type_pattern.match(line)
		#		if file_ext:
		#			file_ext = file_ext.groups()
		#			self.__filetype_registry[file_ext] = f
		#		elif "--START" in line:
		#			break
		#	self.__registered_templates.append(Template(template_filename))
		#except FileNotFoundError:
		#	print ("Could not find file: %s" % self.__template_location +"/"+ template_filename)

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
		contains_registry = ".file_types.db" in os.listdir(self.__template_location)
		if not contains_registry:
			self.create_registry_file()
		else: # Don't update the registry here, instead we will run the updates when a template is not in our database
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
		#print(self.__registered_templates)
		#print(self.__filetype_registry)

