# -*- coding: utf-8 -*-

"""hunpy.hunpy: provides entry point main()."""

__version__ = "0.0.1"


import sys
from .bootstrap import Bootstrap
from .log import Log
import os


def main():
    print("Executing hunpy version %s." % __version__)
    print("List of argument strings: %s" % sys.argv[1:])
    print("Bootstrap and Log:\n%s\n%s" % (Bootstrap, Log))

    project_root_path = os.path.abspath(__file__ + '/../../')
    print(project_root_path)

    bootstrap = Bootstrap()
    while True:
        bootstrap.start()

    # parser = argparse.ArgumentParser(description='Hunpy for ads')
    # parser.add_argument('-u', '--url', help='insert url to process', action='append')
    # parser.parse_args()


