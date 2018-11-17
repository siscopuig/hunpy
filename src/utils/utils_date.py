import datetime



class UtilsDate:


	@staticmethod
	def get_datetime():
		"""

		:return:
		"""
		return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
