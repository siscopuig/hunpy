import datetime



class UtilsDate:


	@staticmethod
	def get_datetime():
		"""

		:return:
		"""
		date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		return date
