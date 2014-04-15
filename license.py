#!/usr/bin/python3

#######################################################################################
# license
#
# license.py
# Written by Evan Wilde
# April 6 2014
# 
# This program will place license agreement information at the top of source code files
# It reads your information from a config file, or requests your information to generate
# the config file
#
#######################################################################################

import argparse
import fileinput
import os
import re
import sys
import time
import multiprocessing
import math

import header
import template_manager

# String pattern
input_pattern = "Username:(.*)email:(.*)"
input_pattern = re.compile(input_pattern)
email_pattern = "[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
email_pattern = re.compile(email_pattern)

#	Colors
class terminal_colors:
	''' Terminal color output definitions '''
	HEADER = '\033[95m'
	BLUE = '\033[34m'
	GREEN = '\033[92m'
	DEBUG = '\033[93m'
	FAIL = '\033[91m'
	END = '\033[0m'

def filechunks (files, threads):
	return [files[i:i+math.ceil(len(files)/threads)] for i in range(0, len(files), math.ceil(len(files)/threads))]  

def chunks (l, n):
	if n < 1:
		n = 1
	return [l[i:i+n] for i in range (0, len(l), n)]

def main():
	args = argparse.ArgumentParser(description = "Add headers to source files.")
	args.add_argument('files', nargs ="+", help = "List of files to add headers to.")
	args.add_argument('-u', '--username', help = "Specify a username to set copyright to. Requires an email be passed as well.")
	args.add_argument('-e', '--email', help = "Specify an email address for the user.")
	args.add_argument('-v', '--verbose',action = "store_true", help = "Outputs verbosely.")
	args.add_argument('--version', action = "version", version = "%(prog)s 0.1")
	args = vars(args.parse_args())
	username = ""
	email = ""

	# Should load this in either from the config file or from the args
	templates = template_manager.template_manager("./templates")

	# If there isn't a configuration file, try scraping it off the arguments
	try:
		config_file = open ("./.license.config", mode = 'r')
		filecontents = str(config_file.read())
		(username, email) = input_pattern.match(filecontents).groups()

		done = False
		replace_string = ""
		rewrite_flag = False

		user_selection = "n"
		if (args['username'] and str(username) != str(args['username'])):
			replace_string += "Username:"
			print ("Original username: ", username, "\nNew username:      ", args['username'])
			while (not done):
				user_selection = input ("Would you like to replace the current username?y/n:")
				if (user_selection is "y"):
					replace_string += args['username']
					username = args['username']
					done = True
					rewrite_flag = True
				elif (user_selection is not "n"):
					print ("Please type y for yes, n for no.")
				else:
					done = True
		else:
			replace_string += "Username:"
			replace_string += username

		done = False
		user_selection = "n"
		if (args['email'] and str(email) != str(args['email'])):
			replace_string += "email:"
			print ("Original email: ", email, "\nNew email:      ", args['email'])
			while (not done):
				user_selection = input ("Would you like to replace the current email?y/n:")
				if (user_selection is "y"):
					replace_string += args['email']
					email = args['email']
					done = True
					rewrite_flag = True
				elif (user_selection is not "n"):
					print ("Please type y for yes, n for no.")
				else:
					done = True
		else:
			replace_string += "email:"
			replace_string += email

		config_file.close()
		if (rewrite_flag):
			config_file = open("./.license.config", mode = 'w')
			config_file.write(replace_string)
	except Exception:
		config_file = open("./.license.config", mode = 'w')
		if (not args['username']):
			username = input("Your Name:")
		else:
			username = args['username']
		if (not args['email']):
			valid = False
			while (not valid):
				email = input("Your Email:")
				if (email_pattern.match(email)):
					valid = True	
		else:
			valid = False
			email = args['email']
			if (email_pattern.match(email)):
					valid = True
			while not valid:
				email = input("Your Email:")
				if (email_pattern.match(email)):
					valid = True
		user_data = "Username:" +  username + "email:" + email
		config_file.write(user_data)

	if (username and not email):
		print(terminal_colors.FAIL + "Email not provided" + terminal_colors.END)
		exit()
	print ("User:", username, "\t\t<" + email + ">")

	# Disabled until threading figured out
	#max_threads = multiprocessing.cpu_count()
	#file_list = filechunks(args['files'], max_threads)

	file_list = list(set(args['files'])) #The list of non-duplicate files
	for src_file in file_list:
		heading = header.header(username, email, src_file)
		print(str(heading.get_file()))
		print(heading)
		print("Associated Template:" + str(templates.search_templates(heading.get_extension())))
		# for each file we need to process, we need to get some information
		# print (src_file)








	#print(file_list)
	#print("Chunks: {0}, Chunk Size: {2} files: {1}".format(len(file_list), len(args['files']), len(file_list[0])) )


if __name__ == '__main__':
	main()


