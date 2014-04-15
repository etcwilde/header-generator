#######################################################################################
# Template manager
#
# template_manager.py
# Written by Evan Wilde
# April 6 2014
# 
# Manges installed license templates and imports new ones. 
#######################################################################################
import files
import os
import pickle
import re
import sys

"""@package docstring
Documentation for module.

More details
"""


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
Template_Include_pattern = "^INCTPYE:(.*)"
Template_Start_pattern = re.compile(Template_Start_pattern) # Necessary?
Template_End_pattern = re.compile(Template_End_pattern) # Necessary?

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

#class template(object):
#	"""Templates contain the metadata for the type of template and the layout for a template"""
#	
#	# Meta-Data
#	include_pattern = ""
#
#	template_file = None
#
#	def load_template(self, templatefile):
#		"""Loads contents of an open file descriptor to a file into the object"""
#		for line in templatefile:
#			print (line)
#
#	def __init__(self, templatename):
#		"""Initializses a template using a string template file input"""
#		self.template_file = fileProperty(templatefile)
#		try:
#			template = open(templatefile)
#			self.load_template(template)
#		except Exception:
#			print("Error loading template file %s" % templatefile)
#			print("Template database corrupted. Delete .file_types.db and run again.")
#			exit()
#

class template:
	#Do I actually want this to be a file? I don't think so.
	#It should contain a file, but not be one necessarily.
	"""Contains the metadata for a template file"""
	template_file = None
	include_pattern = ""
	type_associations = []
	def __init__(self, template_filename):
		"""Initializes a template file"""
		self.template_file = files.fileProperty(template_filename)
		for line in self.template_file:
			print (line)

	def update_associations(self):
		"""Unimplemented
		Updates the metadata headers for the template
		"""
		pass

	def get_associations(self):
		"""Returns the list of associated file types"""
		return type_associations




# Template Manager
#
# Maintains the database of all the templates
class template_manager:
	"""Template manager maintains a database of the installed templates and associated file extensions."""

	__filetype_registry = {}
	__registered_templates = []
	__template_location = ""
	__registry_updated = False

	def create_registry_file(self):
		"""Unimplemented
		Creates a new template registry database
		"""
		pass

	def update_registry_file(self):
		"""Unimplemented
		Updates the template registry database
		Inserts new registry templates
		Removes deleted registry templates
		Updates modified registry templates
		"""
		pass

	def load_registry_file(self):
		"""Unimplemented
		Loads the contents of the registry into the class members
		"""
		pass

	def get_new_templates(self):
		"""Unimplemented
		Returns a list of unique templates that have been put in the template file
		but not registered with the database.
		"""
		pass

	def get_removed_templates(self):
		"""Unimplemented
		Returns a list of unique templates that have been removed from the template file
		but not removed from the database
		"""
		pass

	def get_modified_templates(self):
		"""Unimplemented
		Returns a list of unique templates that have been modified, since their last update in the registry
		"""
		pass

	def add_new_templates(self):
		"""Unimplemented
		Registers all new templates with the registry
		"""
		pass

	def remove_deleted_templates(self):
		"""Unimplemented
		Removes deleted registered templates from the registry
		"""
		pass

	def update_modified_templates(self):
		"""Unimplemented
		Updates modified templates in the registry
		"""
		pass


	def __init__(self, template_location):
		"""Initializses the template manager and database"""
		# This method desperately needs to be refactored
		registry_location = template_location + "/.file_types.db"
		self.__template_location = template_location

		# Does the registry exist?
		contains_registry = ".file_types.db" in os.listdir(template_location)
		if not contains_registry: 
			contains_registry = ".file_types.db" in os.listdir(".")

		# No registry exists, we must create it
		if not contains_registry:
			print ("Created a new registry file")
			print (registry_location)
			for template_file in list_dir_visible(template_location):
				try:
					fobj = files.fileProperty(template_location + "/" + template_file)
					f = fobj.open()
					for line in f:
						file_ext = Template_Type_pattern.match(line)
						if file_ext:
							file_ext = file_ext.groups()[0]
							self.__filetype_registry[file_ext] = fobj
						elif "--START" in line:
							break
					self.__registered_templates.append(fobj)
					f.close()
				except FileNotFoundError:
					print ("Could not find file: %s" % template_location +"/"+ template_file)
			lst = []
			lst.append(self.__registered_templates)
			lst.append(self.__filetype_registry)
			registry_file = open(registry_location, "wb")
			pickle.dump(lst, registry_file)
			registry_file.close()
			print ("Registered Templates:" + str(self.__registered_templates))
			print ("File Types:" + str(self.__filetype_registry))
		else:
			# We shouldn't necessarily need to update the registry,
			# Only if the user requests an unregistered file type
			registry_contents = pickle.load(open(registry_location, "rb"))
			self.__registered_templates = registry_contents[0]
			self.__filetype_registry = registry_contents[1]
			print ("Registered Templates:" + str(self.__registered_templates))
			print ("File Types:" + str(self.__filetype_registry))

	def update_registry(self):
		"""Updates the filetype registry to contains new templates"""
		# This method desperately needs to be refactored
		registry_location = self.__template_location + "/.file_types.db"
		contains_registry = ".file_types.db" in os.listdir(self.__template_location)
		if not contains_registry: 
			contains_registry = ".file_types.db" in os.listdir(".")

		# Check for new files
		registry_contents = pickle.load(open(registry_location, "rb"))
		directory_files = []
		dir_files = list_dir_visible(self.__template_location)
		for filename in dir_files:
			directory_files.append(files.fileProperty(self.__template_location + "/" + filename))
		registry_files = registry_contents[0]
		registry_types = registry_contents[1]

		updated_files = []
		for f in directory_files:
			for f2 in registry_files:
				print("Directory File: {0} -- {1}\t Registry File: {2} -- {3}".format(f.get_file(), f.get_ctime(), f2.get_file(), f.get_ctime()))
				if (f.get_filepath() == f2.get_filepath()):
					print ("Same Kind")
				if (f == f2) and (f.get_ctime != f2.get_ctime):
					updated_files.append(f2)


		new_files = list(set(directory_files) - set(registry_files))
		removed_files = list(set(registry_files) - set(directory_files))
		print ("\tNew Files:\t " + str(new_files))
		print ("\tRemoved Files:\t " + str(removed_files))
		print ("\tUpdated Files:\t " + str(updated_files))
		print("Adding New Files!")
		for fname in new_files:
			f = fname.open("r")
			if f:
				for line in f:
					file_ext = Template_Type_pattern.match(line)
					if file_ext:
						# Register the file extensions
						file_ext = file_ext.groups()[0]
						self.__filetype_registry[file_ext] = fname

					elif "--START" in line:
						break
			# Regsiter the template file
			else:
				print("File Deleted or Incorrect Permissions")
			self.__registered_templates.append(fname)

		print("\tTemplates:\t",self.__registered_templates)
		print("\tAssociation:\t", self.__filetype_registry)
		print("Removing Deleted Files!")
		for fname in removed_files:
			print (fname)
		print("\tTemplates:\t",self.__registered_templates)
		print("\tAssociation:\t", self.__filetype_registry)




	def search_templates(self, file_extension):
		"""Finds the corresponding template file for the extension"""
		# If we can't find the file_type immediately,
		# then we need to go out and update the database and see if we can find it. 
		# This can be made better though, so that it will only go out once... Maybe updateing
		# 	the database at the initial run is better? That way we don't have to worry about going
		# 	out for each file that we run across (say if none of the files are of a registered type, 
		#	nor want the to be text files, compiled files, etc....)

		try:
			return self.__filetype_registry[file_extension]
		except KeyError:
			# Hacky way of ensuring we only update once...
			if not self.__registry_updated:
				self.update_registry()
				self.__registry_updated = True
			else:
				print ("No registered file for: {0}".format(file_extension))
				return None
			try:
				return self.__filetype_registry[file_extension]
			except KeyError:
				print ("No registered file for: {0}".format(file_extension))
				return None



#
#				# Now read each template file and load the associated file extensions into the database
#
#			except Exception:
#				print ("Error: Cannot create registry file.")
#				exit()
#		#Registry does exist, lets find out which file our template is in




