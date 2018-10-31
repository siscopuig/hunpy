import logging
import os
import datetime



class Log:

	# https://docs.python.org/3/library/logging.html
	# https://docs.python.org/3/howto/logging-cookbook.html


	# Formatter
	# '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

	def __init__(self) :

		self.log_filename = ''
		self.log_filepath = ''
		self.formatter = ''
		self.string_format = '%(asctime)s - %(levelname)s - %(message)s'
		self.date_format = "%Y-%m-%d_%H:%M:%S"

		# Creates log filename & filepath
		self.create_log_filepath()

		# Get an instance from logging
		self.logger = logging.getLogger(__name__)


	def create_log_filepath(self):

		dir = '../log/'
		name = 'hunpy'
		date = datetime.datetime.now().strftime(self.date_format)
		self.log_filename = '{name}_{date}.log'.format(name=name, date=date)
		abs_filepath = os.path.abspath(dir)
		self.log_filepath = abs_filepath + '/' + self.log_filename

		# Create file in log directory
		try:
			if not os.path.exists(abs_filepath):
				os.makedirs(abs_filepath)
		except OSError:
			print('Error: Creating directory. ' + abs_filepath)


	def open(self):


		self.logger.setLevel(logging.DEBUG)
		self.formatter = logging.Formatter(self.string_format)


		fh = logging.FileHandler(filename=self.log_filepath, mode='a', encoding=None, delay=False)
		fh.setLevel(logging.DEBUG)
		fh.setFormatter(self.formatter)


		sh = logging.StreamHandler()
		sh.setLevel(logging.DEBUG)
		sh.setFormatter(self.formatter)


		self.logger.addHandler(fh)
		self.logger.addHandler(sh)


	def set_level(self, level):
		"""
		Set the logging level of this logger.
		level must be an int or a str.

		(DEBUG, INFO, WARNING, ERROR, CRITICAL)

		:param level:
		:return:
		"""

		self.logger.setLevel(level)


	def debug(self, *args, **kwargs):
		"""

		:param args:
		:param kwargs:
		:return:
		"""

		logging.LoggerAdapter(self.logger, extra='').debug(*args, **kwargs)


	def info(self, *args, **kwargs):
		"""

		:param args:
		:param kwargs:
		:return:
		"""

		logging.LoggerAdapter(self.logger, extra='').info(*args, **kwargs)


	def warning(self, *args, **kwargs):
		"""

		:param args:
		:param kwargs:
		:return:
		"""

		logging.LoggerAdapter(self.logger, extra='').warning(*args, **kwargs)


	def error(self, *args, **kwargs):
		"""

		:param args:
		:param kwargs:
		:return:
		"""

		logging.LoggerAdapter(self.logger, extra='').error(*args, **kwargs)


	def critical(self, *args, **kwargs):
		"""

		:param args:
		:param kwargs:
		:return:
		"""

		logging.LoggerAdapter(self.logger, extra='').critical(*args, **kwargs)


	def exception(self, *args, **kwargs):
		"""

		:param args:
		:param kwargs:
		:return:
		"""

		logging.LoggerAdapter(self.logger, extra='').exception(*args, **kwargs)


	def close(self):

		self.info('Log End')

		handlers = self.logger.handlers
		for handler in handlers:
			handler.close()
			self.logger.removeHandler(handler)


