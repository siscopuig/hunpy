from os import path, makedirs


def create_directory(abs_filepath):
	try:
		if not path.exists(abs_filepath):
			makedirs(abs_filepath)
	except OSError:
		print('Error: Creating directory. ' + abs_filepath)


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

