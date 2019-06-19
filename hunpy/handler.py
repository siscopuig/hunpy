from .driver import Driver
from .page import Page
from .log import Log
from .module_manager import ModuleManager
from .utils.utils_date import UtilsDate
import traceback
import subprocess
import sys


class Handler:

    processors = None

    def __init__(self, config, datasource):

        self.log = Log()
        self.config = config
        self.datasource = datasource
        self.driver = None
        self.page = None

    def search(self):

        date = UtilsDate.get_date()
        urls = self.datasource.get_urls()

        for url in urls:

            # For debugging purposes:
            # url['url'] = 'http://localhost:63342/hunpy/lab/html_templates/html_main_document.html'
            # url['id']  = 1

            try:

                # Get driver instance
                if self.driver is None:
                    self.driver = Driver(self.config)
                    self.log.info('Chromedriver started')
                    self.driver.start(headless=True)

                # Open url in browser
                self.driver.open(url['url'], 1)
                self.log.info('Page opened: {}'.format(url['url']))

                # Open a page instance
                self.page = Page(self.driver, url['id'], url['url'])

                # Load processors
                module_manager = ModuleManager(self.driver, self.config,
                                               self.datasource)
                module_manager.create_processors(self.config['processors'])

                # Iterate processors (tuple)
                for name, processor in module_manager.get_processors().items():
                    processor.process_start(self.page, processor_name=name)

                # Count cycle
                self.datasource.count_cycle(url['id'], date)

            except Exception as e:

                # For debugging purposes only
                print(traceback.format_exc())
                exception = str(e).replace('\n', '')

                # At this point, if an exception is thrown kill chromedriver processes
                self.reset_chromedriver()
                self.log.error(
                    'Stopped chromedriver by exception: {}'.format(exception))

                # Reset driver
                self.driver = None

    def reset_chromedriver(self):

        try:
            retcode = subprocess.call(["pkill", "-f", "chromium-browser"])

            if retcode < 0:
                self.log.warning(
                    'Child was terminated by signal, -retcode: ({})'.format(
                        -retcode, file=sys.stderr))
            else:
                self.log.warning('Child returned, retcode:({})'.format(
                    retcode, file=sys.stderr))

        except OSError as e:
            self.log.error('Execution failed: OSError: {}'.format(
                e, file=sys.stderr))
