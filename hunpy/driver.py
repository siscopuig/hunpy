# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
import selenium.common.exceptions as sce
from selenium.webdriver.support import expected_conditions as expect_cond
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from hunpy.utils.utils_files import get_project_root_abs_path


def ewe(none_result=True, common_exception_result=False):
    """
    Execute without exceptions
    """

    def action(func):
        """
        :param func:
        :return: wrapper function
        """

        def wrapper(self, *args, **kwargs):
            """
            Some functions do not return anything unless is an exception.
            We could assume that if None is True. E.g. switch_to_frame()

            :param self:
            :param args:
            :param kwargs:
            :return: wrapper
            """
            try:

                # print(func)
                result = func(self, *args, **kwargs)

                if result is None:
                    return none_result
                else:
                    return result

            except sce.NoSuchElementException:
                return common_exception_result

            except TimeoutException as e:
                raise TimeoutException(e)

            except self.common_exceptions:
                return common_exception_result

        return wrapper

    return action


class Driver:

    common_exceptions = (

        # Thrown when window target to be switched doesn't exist.
        sce.NoSuchWindowException,

        # Thrown when frame target to be switched doesn't exist.
        sce.NoSuchFrameException,

        # Thrown when the attribute of element could not be found.
        sce.NoSuchAttributeException,

        # Stale means the element no longer appears on the DOM of the page.
        sce.StaleElementReferenceException,

        # Thrown when an element is present on the DOM, but
        # it is not visible, and so is not able to be interacted with.
        sce.ElementNotVisibleException,

        # Thrown when an element is present in the DOM but interactions
        # with that element will hit another element do to paint order
        sce.ElementNotInteractableException,

        # Thrown when the selector which is used to find an element does not
        # return a WebElement. Currently this only happens when the selector
        # is an xpath expression and it is either syntactically invalid
        # (i.e. it is not a xpath expression) or the expression does not
        # select WebElements (e.g. "count(//input)").
        sce.InvalidSelectorException,

        # Thrown when frame or window target to be switched doesn't exist.
        sce.InvalidSwitchToTargetException,

        # Thrown when the target provided to the `ActionsChains` move()
        # method is invalid, i.e. out of document.
        sce.MoveTargetOutOfBoundsException,
    )

    def __init__(self, config):

        self.config = config

        self.driver = None

        self.chrome_options = None


    def start_driver(self, headless=False):

        # Set chrome options from config
        self.set_chrome_options(headless)

        # Get webdriver instance
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)

        # Set chrome viewport
        self.driver.set_window_size(int(self.config['chrome.window.width']),
                                    int(self.config['chrome.window.height']))

        # Waiting time before timeout exception is thrown
        self.driver.set_page_load_timeout(int(
            self.config['page.load.timeout']))

        # Waiting for any request made. E.g. get element attribute
        self.driver.implicitly_wait(0)


    def set_chrome_options(self, headless):

        self.chrome_options = Options()

        self.chrome_options.binary_location = self.config['chrome.binary.location']

        # Sets user profile path
        abs_path = get_project_root_abs_path(self.config['chrome.option.profile.path'])
        self.chrome_options.add_argument('--user-data-dir={}'.format(abs_path))

        # Sets user agent
        self.chrome_options.add_argument(self.config['chrome.user.agent'])

        # Sets ignore ssl errors
        self.chrome_options.add_argument(
            self.config['chrome.option.ignore.ssl.errors'])

        # Unable dns-prefetch
        self.chrome_options.add_argument(
            self.config['chrome.option.dns.prefetch.disable'])

        # Disable infobars
        self.chrome_options.add_argument(
            self.config['chrome.option.disable.infobars'])

        # Disable gpu
        self.chrome_options.add_argument(
            self.config['chrome.option.disable.gpu'])

        # Disable plugins
        self.chrome_options.add_argument(
            self.config['chrome.option.disable-plugins'])

        # Unable sandbox
        self.chrome_options.add_argument(
            self.config['chrome.option.nosandbox'])

        # Disable session crashed bubble
        self.chrome_options.add_argument(
            self.config['chrome.option.disable.crashed.bubble'])

        # Disable notifications
        self.chrome_options.add_argument(
            self.config['chrome.option.disable.notifications'])

        # Enable headless mode
        if headless:
            self.chrome_options.add_argument(
                self.config['chrome.option.headless'])

        # Experimental options
        prefs = {'profile.default_content_setting_values.notifications': 2}
        self.chrome_options.add_experimental_option('prefs', prefs)

    @ewe()
    def get_driver(self):

        if self.driver is None:
            self.start_driver()
        return self.driver

    @ewe()
    def open(self, url, wait=None):

        self.get_driver().get(url)

        if wait:
            time.sleep(wait)


    @ewe()
    def quit(self):

        self.driver.quit()


    @ewe([], [])
    def find_elements_by_xpath(self, xpath):

        return self.get_driver().find_elements_by_xpath(xpath)


    @ewe(None, None)
    def find_element_by_xpath(self, xpath):

        return self.get_driver().find_element_by_xpath(xpath)


    @ewe()
    def find_element_parent_by_child(self, child_element, xpath):

        return child_element.find_element_by_xpath(xpath)


    @ewe('', '')
    def get_element_size(self, element):

        return element.size['width'], element.size['height']


    @ewe('', '')
    def get_element_location(self, element):

        return element.location['x'], element.location['y']


    @ewe('', '')
    def get_element_attribute(self, element, attr):

        return element.get_attribute(attr)


    @ewe()
    def close(self):

        self.get_driver().close()


    @ewe()
    def get_window_size(self):

        return self.driver.get_window_size()


    @ewe()
    def switch_to_default_content(self):

        self.get_driver().switch_to.default_content()


    @ewe()
    def switch_to_window_default_content(self, window):

        if self.switch_to_window(window):
            return self.switch_to_default_content()
        return False


    @ewe()
    def switch_to_iframe(self, element):

        self.get_driver().switch_to.frame(element)


    @ewe(None, None)
    def find_child_element_by_xpath(self, xpath, parent_element):

        return parent_element.find_element_by_xpath(xpath)


    @ewe()
    def is_element_displayed(self, element):
        """
        Whether the element is visible to a user
        """
        return element.is_displayed()


    @ewe()
    def is_visibility_of_element_located(self, xpath):
        """
        Given the generated xpath reference find the element of an element
        previously seen. Does not work at the moment!!
        """
        WebDriverWait(
            self.get_driver(), 2, 0.2).until(
                expect_cond.visibility_of_element_located(
                    self.get_driver().find_element_by_xpath(xpath)))


    @ewe()
    def wait_for_element_visibility(self, element):
        """
        Waits for an element until becomes visible

        :param element:
        :return: the (same) WebElement once it is visible
        """
        return WebDriverWait(self.get_driver(), 2,
                             0.2).until(expect_cond.visibility_of(element))


    @ewe()
    def refresh_window(self):

        self.get_driver().execute_script("location.reload()")


    @ewe([], [])
    def get_window_handle(self):
        """
        Returns the handles of all windows within the current session.
        """

        return self.get_driver().window_handles


    @ewe('', '')
    def get_main_window_handle(self):
        """
        :return: 'CDwindow-552D2F0FD1B1B6C1B5FECCDE486232A7'
        """

        return self.get_driver().window_handles[0]


    @ewe()
    def switch_to_window(self, window):

        self.get_driver().switch_to.window(window)


    @ewe()
    def save_screenshot(self, filename):
        """
        Gets the screenshot of the current element as a binary data.
        """
        self.get_driver().save_screenshot(filename)


    @ewe()
    def close_window_except_main(self, windows):
        """
        Close all tabs opened except (0)
        """
        for i, window in enumerate(windows):
            if i != 0:
                self.switch_to_window(window)
                self.driver.close()


    @ewe()
    def execute_javascript(self, script):

        driver = self.get_driver()

        return driver.execute_script(script)


    @ewe()
    def click_on_element(self, element):
        """
        On chrome, pressing the middle button of the mouse links are forced
        to open a new tab. (Appears that do not work anymore)
        Open links in a new tab -> Send Keys -> Ctrl + Shift + click

        :return None
        """

        # Is element visible?
        element = self.wait_for_element_visibility(element)
        if not element:
            return None

        ActionChains(self.get_driver()).move_to_element(element).\
            key_down(Keys.COMMAND).click().key_up(Keys.COMMAND).perform()


    @ewe('', '')
    def get_current_url(self):

        return self.get_driver().current_url


    @ewe()
    def move_to_element(self, element):

        # element = self.wait_for_element_visibility(element)
        # if not element:
        #     return None

        ActionChains(self.get_driver()).move_to_element(element).perform()


    @ewe()
    def open_new_tab(self):
        """
        There is a bug in chromedriver that prevent chrome
        to open a new tab sending keys (CONTROL + "t")
        """
        # element = self.find_element_by_xpath('.//body')
        # ActionChains(
        #   self.get_driver()).send_keys(
        #       Keys.COMMAND + "t").click(element).perform()
        # ActionChains(self.get_driver()).key_down(Keys.CONTROL).click(element)\
        # 	.send_keys('t').perform()
