import datetime


class UtilsDate:

	@staticmethod
	def get_datetime():
		return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	@staticmethod
	def get_date():
		return datetime.datetime.today().strftime('%Y-%m-%d')