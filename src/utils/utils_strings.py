
from os import path
import re

class UtilsString:



	@staticmethod
	def match_string_in_list(string, list):
		"""

		"""
		# Convert strings to casefolded strings for caseless matching
		# (Is an aggressive lower case)
		string = string.casefold()


		for element in list:
			str = ''.join(element)
			if str == string:
				return True
		return False


	@staticmethod
	def match_string_list_in_list(src, list):

		src = src.casefold()
		exploded = src.split('/')

		for string in exploded:
			for str in list:
				if string == str:
					return True
		return False


	@staticmethod
	def get_domain(url):
		"""
		Get domain from urls like http://localhost:63342/hunpy/ or
		http://www.localhost:63342/hunpy/. Returns 'localhost:63342'
		"""

		if 'www' in url:
			url = url.replace('www.', '')

		exploded = url.split('/')

		for i, piece in enumerate(exploded):
			if 'http' in piece:
				exploded.pop(i)
				break

		# @todo: IndexError: list index out of range

		if len(exploded) >= 2:
			return exploded[1]

		return ''


	@staticmethod
	def get_abs_path(relative_path):
		# path.abspath():
		#
		# simply removes things like . and .. from the path giving a full path
		# from the root of the directory tree to the named file (or symlink)

		# path.expandruser():
		#
		# On Unix and Windows, return the argument with an initial component of ~ or ~user
		# replaced by that user’s home directory.
		#
		# On Unix, an initial ~ is replaced by the environment variable HOME
		# if it is set; otherwise the current user’s home directory is looked up
		# in the password directory through the built-in module pwd.
		# An initial ~user is looked up directly in the password directory.
		#
		# On Windows, HOME and USERPROFILE will be used if set,
		# otherwise a combination of HOMEPATH and HOMEDRIVE will be used.
		# An initial ~user is handled by stripping the last directory component
		# from the created user path derived above.
		#
		# If the expansion fails or if the path does not begin with a tilde,
		# the path is returned unchanged.
		return path.abspath(path.expanduser(relative_path))


	@staticmethod
	def match_placement(placements, width, height):
		"""
		"""
		for size in placements:
			if size[0] == width and size[1] == height:
				return True
		return False


	@staticmethod
	def strip_string(string, delimeter=None):
		"""
		Strip any characters after the delimeter char

		:param string:
		:param delimeter:
		:return:
		"""
		exploded = string.split(delimeter)

		if len(exploded) == 1:
			return string

		exploded.pop(-1)

		return exploded[0]



	@staticmethod
	def get_url_from_string(string):
		"""
		Finds a url inside a string

		:param string:
		:return: None or url
		"""

		# Return a list of all non-overlapping matches in the string.
		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]'
						  '|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
		if not urls:
			return None

		# Returns last element
		return urls.pop(-1)


	@staticmethod
	def return_test():

		request = {
			"status": 200,
			"content_type": "text/html"
		}
		src = 'source'

		return src, request


#############################
#
# a, b = UtilsString.return_test()
# print(a, b)

# str = 'https://www.clearbridge.com/global-esg.html?cmpid=cbieu18_eur_web_penage_ros_728x90_wtr'
# UtilsString.strip_string(str, '?')



# str = """"EBG.ads["1075102305_6674910311817199"].onImageClick("1075102305_6674910311817199",
# 		true,"ebDefaultImg_1075102305_6674910311817199",
# 		"https://www.clearbridge.com/global-esg.html?cmpid=cbieu18_eur_web_penage_ros_728x90_wtr",
# 		"", "")"
# """
#
# url = UtilsString.get_url_from_string(str)
# print(url)



# src = 'http://localhost:63342/hunpy/lab/html_templates/html_main_document.html'
# ignored_list = ['safeframe', 'google', 'localhost:63342']
# domain = UtilsString.get_domain('http://localhost:63342/hunpy/lab/html_templates/html_main_document.html')
# match_string_in_list(domain, ignored_list)
# UtilsString.match_string_list_in_list(src, ignored_list)