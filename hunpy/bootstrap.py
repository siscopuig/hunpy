# -*- coding: utf-8 -*-

import traceback
import subprocess
import sys
from hunpy.driver import Driver
from hunpy.page import Page
from hunpy.log import Log
from hunpy.module_manager import ModuleManager


class Bootstrap:

    processors = None

    def __init__(self, config, datasource):

        self.log = Log()
        self.config = config
        self.datasource = datasource
        self.driver = None
        self.page = None
        self.urls = {}


    def search(self, urls, arg_headless):

        for url_id, url in urls.items():

            try:

                # Get driver instance
                if self.driver is None:
                    self.driver = Driver(self.config)
                    self.log.info('Chromedriver started')
                    self.driver.start_driver(headless=arg_headless)

                # Open url in browser
                self.driver.open(url, 1)
                self.log.info('Page opened: {}'.format(url))

                # Open a page instance
                self.page = Page(self.driver, url_id, url)

                # Load processors
                module_manager = ModuleManager(self.driver, self.config,self.datasource)
                module_manager.create_processors(self.config['processors'])

                # Iterate processors (tuple)
                for name, processor in module_manager.get_processors().items():
                    processor.process_start(self.page, processor_name=name)

            except Exception as exception:
                exception = str(exception).replace('\n', '')
                self.log.error(f"Exception caught on Bootstrap: ({exception})")

                # At this point, if an exception is thrown kill chromedriver processes
                self.reset_chromedriver()
                self.log.error('Stopped chromedriver by exception: {}'.format(exception))

                # Reset driver
                self.driver = None

        self.driver.close()
        self.driver.quit()


    def reset_chromedriver(self):

        try:
            subprocess.call(["pkill", "-f", "chromium-browser"])
            subprocess.call(["pkill", "-f", "chromedriver"])
        except OSError as e:
            self.log.error('Execution failed: OSError: {}'.format(
                e, file=sys.stderr))
