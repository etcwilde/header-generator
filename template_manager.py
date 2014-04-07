#######################################################################################
# Template manager
#
# template_manager.py
# Written by Evan Wilde
# April 6 2014
# 
# Manges installed license templates and imports new ones. 
#######################################################################################
import os
import pickle
import re
import sys

#################
# Regex patterns
#################
#--[Input File Patterns] ----------------------------
file_name_pattern = "^([a-zA-Z0-9_-]*)\.([a-zA-Z0-9]*)$"
file_name_pattern = re.compile(file_name_pattern)

#--[Template File Patterns] -------------------------
Template_Type_pattern = "^TYPE:(.*)"
Template_Include_pattern = "^INCTPYE:(.*)"
Template_Type_pattern = re.compile(Template_Type_pattern)
Template_Include_pattern = re.compile(Template_Include_pattern)


class template_manager(object):
	"""docstring for template_manager"""
	def __init__(self, header_info, template_location):
		filetype_registry = {}
		registered_templates = []
		registry_location = template_location + ".file_types.db"

		# Does the registry exist?
		contains_registry = ".file_types.db" in os.listdir(template_location)
		if not contains_registry: 
			contains_registry = ".file_types.db" in os.listdir(".")

		# No registry exists, we must create it
		if not contains_registry:
			try:
				registry_file = open(registry_location, "wb")
			except Exception:
				print ("Error: Cannot create registry file.")
				exit()
		#Registry does exist, lets find out which file our template is in
		registry_contents = pickle.load(open(registry_location, "rb"))


	def generate_header(self, filename):


