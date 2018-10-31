from os import path, makedirs



def create_directory(self, abs_filepath):
	try:
		if not path.exists(abs_filepath):
			makedirs(abs_filepath)
	except OSError:
		print('Error: Creating directory. ' + abs_filepath)
