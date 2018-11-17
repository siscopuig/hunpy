
import re

class UtilsString:



	@staticmethod
	def match_string_in_list(string, string_list, name_list):

		# @todo:
		# This needs to be rewritten in order to use numpy arrays.
		# An error is thrown occasionally when a string is compared
		# from a string coming from a numpy array. E.g.
		# 	ValueError: The truth value of an array with more than
		# 	one element is ambiguous. Use a.any() or a.all()
		#
		# Apparently the trick here is not compare strings using == but
		# this method instead: if (s is string)



		# Convert strings to casefolded strings for caseless matching
		# (Is an aggressive lower case)
		string = string.casefold()

		try:

			for element in string_list:
				str = ''.join(element.casefold())
				if str in string:
					print('match_string_in_list({}) str: {} in string: {}'.format(name_list, str, string))
					return True

		except ValueError as ex:
			print(ex)

		return False


	@staticmethod
	def match_string_parts_in_list(src, string_list, name_list):

		# match_string_parts_in_list(ignore_path) string: ads in str: uploads
		# https://s0.2mdn.net/ads/richmedia/studio/pv2/60817163/20180903024843963/index.html

		# 'is' is used for identity comparison, while == is used for equality comparison

		# So, when you have two string literals (words that are literally typed into your
		# program source code, surrounded by quotation marks) in your program that have
		# the same value, the Python compiler will automatically intern the strings, making
		# them both stored at the same memory location. (Note that this doesn't always happen,
		# and the rules for when this happens are quite convoluted, so please don't rely
		# on this behavior in production code!)
		#
		# Since in your interactive session both strings are actually stored in the same
		# memory location, they have the same identity, so the is operator works as expected.
		# But if you construct a string by some other method (even if that string contains
		# exactly the same characters), then the string may be equal, but it is not
		# the same string -- that is, it has a different identity, because it is stored
		# in a different place in memory.


		try:

			src = src.casefold()
			exploded = src.split('/')

			for string in exploded:
				for str in string_list:

					if string and string in str.casefold() and string == str.casefold():
						print('match_string_parts_in_list({}) string: {} in str: {}'.format(name_list, string, str))
						return True

		except ValueError as ex:
			print(ex)

		return False


	@staticmethod
	def get_domain(url):
		"""
		Get domain from urls like http://localhost:63342/hunpy/ or
		http://www.localhost:63342/hunpy/. Returns 'localhost:63342'
		"""
		if url is None:
			print(0)

		if 'www' in url:
			url = url.replace('www.', '')

		exploded = url.split('/')

		for i, piece in enumerate(exploded):
			if 'http' in piece:
				exploded.pop(i)
				break

		if len(exploded) >= 2:
			return exploded[1]

		return ''


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

		E.g. https://adclick.g.doubleclick.net/pcs/click?xai=AKAOjsvhOqNiIi3Zv-
		JwQKu7K3VwVXzzhphDRT4O8FZ48g9A3QHmZ0m-m58ugEOY7GrBMuA_T4DfhkyDRm12fX8BlFD
		JK3df8lhzM9kIzjWg2w342TC7S3B1UFUH6qc-qj8ElBwxvEZJ7UiGVqgi5pJHqEVq8i9kNcxDLZ
		FqdmUT4DexaYprDksioGNurfK-RQ2qaFdb21kwvEhJ9x9Px1Wu3kLIRHhIh71kLpOLsLWO7t9vD
		3w1WfmlWrcpuUvLfd31zQy2&sai=AMfl-YSmUDAw5oZbgx8BID9_3GzlxdLUM-sCS7oadMMYImbQ
		YLnlaWVdI9DY0zOTl1zgla8uu9HGyIuv_gQHP2ExfND_6Vbm29FXV3pHLu6_5wQsZ0-mOFLxgssHL
		XUj&sig=Cg0ArKJSzAcOvYMZk5ZOEAE&urlfix=1&adurl=
		https://servedby.flashtalking.com/click/1/98145;3371049;2367840;210;0/
		?ft_impID=6A4E4B98-DA0F-88F7-361E-3BA1078F0145&g=3947060DBD153D&random=55963&ft_width=300&ft_height=600&url=
		https://www.rlam.co.uk/Home/Intermediaries/Products/Fixed-Income/OEICs/Monthly-Income-Bond-Fund/
		?utm_source=FTAdviser&utm_medium=Half%20Page&utm_campaign=MIB%202018

		:param string:
		:return: None or url
		"""

		# Return a list of all non-overlapping matches in the string.
		# urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)

		# Outputs: ['https://adclick.g.doubleclick.net', 'https://servedby.flashtalking.com', 'https://www.rlam.co.uk']
		# urls = re.findall('http[s]?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', string)

		# Outputs: [
		# 	'https://adclick.g.doubleclick.net/pcs/click',
		#	'https://servedby.flashtalking.com/click/1/98145',
		#	'https://www.rlam.co.uk/Home/Intermediaries/Products/Fixed-Income/OEICs/Monthly-Income-Bond-Fund/'
		# ]
		urls = re.findall('http[s]?://(?:(?!http[s]?://)[a-zA-Z]|[0-9]|[$\-_@.&+/]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)

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
# src = 'https://adclick.g.doubleclick.net/pcs/click?xai=AKAOjsvhOqNiIi3Zv-JwQKu7K3VwVXzzhphDRT4O8FZ48g9A3QHmZ0m-m58ugEOY7GrBMuA_T4DfhkyDRm12fX8BlFDJK3df8lhzM9kIzjWg2w342TC7S3B1UFUH6qc-qj8ElBwxvEZJ7UiGVqgi5pJHqEVq8i9kNcxDLZFqdmUT4DexaYprDksioGNurfK-RQ2qaFdb21kwvEhJ9x9Px1Wu3kLIRHhIh71kLpOLsLWO7t9vD3w1WfmlWrcpuUvLfd31zQy2&sai=AMfl-YSmUDAw5oZbgx8BID9_3GzlxdLUM-sCS7oadMMYImbQYLnlaWVdI9DY0zOTl1zgla8uu9HGyIuv_gQHP2ExfND_6Vbm29FXV3pHLu6_5wQsZ0-mOFLxgssHLXUj&sig=Cg0ArKJSzAcOvYMZk5ZOEAE&urlfix=1&adurl=https://servedby.flashtalking.com/click/1/98145;3371049;2367840;210;0/?ft_impID=6A4E4B98-DA0F-88F7-361E-3BA1078F0145&g=3947060DBD153D&random=55963&ft_width=300&ft_height=600&url=https://www.rlam.co.uk/Home/Intermediaries/Products/Fixed-Income/OEICs/Monthly-Income-Bond-Fund/?utm_source=FTAdviser&utm_medium=Half%20Page&utm_campaign=MIB%202018'
# url = UtilsString.get_url_from_string(src)
# print(url)
