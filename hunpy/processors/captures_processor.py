# -*- coding: utf-8 -*-

import os
import io
import time
from PIL import Image, ImageChops
from hunpy.log import Log
from hunpy.processor import Processor
from hunpy.advert import AdvertState
from hunpy.utils.utils_date import UtilsDate
from hunpy.utils.utils_requests import  UtilsRequest
from hunpy.captures import Captures


class CapturesProcessor(Processor):

    def __init__(self, driver, config, datasource):

        super().__init__(driver, config, datasource)

        self.driver = driver

        self.log = Log()

        self.working_dir = config['working.dir']

        self.localhost_tmpl_path = config['localhost.tmpl.path']

        self.tmpl_path = config['tmpl.path']

        self.headers = config['headers']

        self.utilrequest = UtilsRequest(self.config['http_bad_request'], self.config['headers'])


    def process(self, page):

        if not page.adverts:
            self.log.warning('No adverts to process in CapturesProcessor')
            return False

        print(f"N of adverts to process in Captures: ({len(page.adverts)})")

        batch = self.extract_process_list(page.adverts)

        if batch:

            for capture in batch:

                state = capture.state
                if state == AdvertState.EXISTING:
                    continue

                if capture.type == 'static':
                    self.process_static(capture)

                if capture.type == 'dynamic':
                    self.process_dynamic(capture)

                if capture.type == 'screenshot':
                    self.process_screenshot_element(capture)

        # For debugging purposes only
        for capture in batch:
            self.log.debug(capture.__str__())


    def extract_process_list(self, adverts):

        batch = []

        for advert in adverts:

            capture = Captures()

            finfo = advert.finfo
            uuid = advert.uid
            date = UtilsDate.get_date()

            capture.width = advert.size[0]
            capture.height = advert.size[1]
            capture.src = advert.src
            capture.state = advert.state

            capture.tmp_path = '/'.join([self.working_dir, 'captures', 'tmp'])

            if not finfo == 'text/html':
                capture.type = 'static'
                capture.finfo = advert.finfo
                capture.ext = finfo.split('/')[1]
                capture.fname = '.'.join([uuid, capture.ext])
                capture.tmp_filepath = '/'.join([capture.tmp_path, capture.fname])
                capture.dest_path = '/'.join([self.working_dir, 'captures', 'store', date])
                capture.dest_filepath = '/'.join([capture.dest_path, capture.fname])
                advert.filepath = capture.dest_path

            else:
                capture.type = 'dynamic'
                capture.ext = 'png'
                capture.finfo = finfo
                capture.fname = '.'.join([uuid, 'png'])
                capture.tmp_filepath = '/'.join([capture.tmp_path, capture.fname])
                capture.dest_path = '/'.join([self.working_dir, 'captures', 'store', date])
                capture.dest_filepath = '/'.join([capture.dest_path, capture.fname])
                capture.iframe_xpath = advert.xpath
                advert.filepath = capture.dest_filepath

                if not advert.is_known_placement:
                    capture.type = 'screenshot'

            batch.append(capture)

        return batch


    def process_dynamic(self, capture):

        try:

            # Creates dir if not exists
            if not os.path.exists(capture.dest_path):
                os.makedirs(capture.dest_path)

            # Truncate file (delete content)
            with open(self.tmpl_path, 'w') as f:
                f.truncate(0)

            # Write html content in file
            html_template = self.build_template(capture.src, capture.width, capture.height)
            with open(self.tmpl_path, 'w') as f:
                f.write(html_template)

            self.driver.execute_javascript('window.open("{}","_blank");'.format(self.localhost_tmpl_path))
            time.sleep(1)

            windows = self.driver.get_window_handle()


            if len(windows) == 2:

                self.driver.switch_to_window(windows[1])

                # Get iframe position
                element = self.driver.find_element_by_xpath('//iframe')
                if not element:
                    self.log.debug('CapturesProcessor:process_dynamic not iframe element found')

                else:
                    pos = dict()
                    pos['x'] = element.rect['x']
                    pos['y'] = element.rect['y']

                    self.driver.save_screenshot(capture.tmp_filepath)
                    image = Image.open(io.FileIO(capture.tmp_filepath))
                    image = image.crop((int(pos['x']), int(pos['y']), int(capture.width), int(capture.height)))
                    image_rgb = image.convert('RGB')
                    image_rgb.save(capture.dest_filepath, format('PNG'))

                    os.remove(capture.tmp_filepath)

                    # Checks whether the saved image is blank(white)
                    saved_image = Image.open(io.FileIO(capture.dest_filepath))

                    if not ImageChops.invert(saved_image).getbbox():
                        self.log.debug(f"Saved image from source: ({capture.src}) is blank")
                        self.process_screenshot_element(capture)

            self.driver.close_window_except_main(windows)

        except Exception as exception:
            self.log.error(f'Exception on CapturesProcessor: {exception}')


    def process_screenshot_element(self, capture):

        if not capture.iframe_xpath:
            self.log.debug(f"CapturesProcessor:process_screenshot_element iframe_xpath missing")
            return False

        element = self.driver.find_element_by_xpath(capture.iframe_xpath)

        if element:

            # Moves to the middle of the element
            self.driver.move_to_element(element)
            time.sleep(1)

            # Saves a screenshot browsers viewport
            self.driver.save_screenshot(capture.tmp_filepath)

            # Get browser height
            scroll_y = self.driver.execute_javascript("return window.scrollY;")
            location = element.location
            size = element.size
            left   = location['x']
            top    = location['y'] - scroll_y
            right  = location['x'] + size['width']
            bottom = location['y'] + size['height'] - scroll_y

            # Crop element
            im = Image.open(io.FileIO(capture.tmp_filepath))
            im = im.crop((int(left), int(top), int(right), int(bottom)))
            im.save(capture.dest_filepath, format('PNG'))

            # Removes file in tmp dir
            os.remove(capture.tmp_filepath)

        else:
            self.log.error(f"Not element found by xpath: ({capture.iframe})")


    def process_static(self, capture):

        response = self.utilrequest.get_http_response(capture.src)
        if not response:
            return False

        if response['finfo'] != capture.finfo:
            self.log.error(f"Advert finfo: ({capture.finfo}) not equal to response({response['finfo']})")
            return False

        try:

            # Save img on tmp dir
            with Image.open(io.BytesIO(response['request'].content)) as img:
                img.save(capture.tmp_filepath)

            # Create path in captures
            if not os.path.exists(capture.dest_path):
                os.makedirs(capture.dest_path)

            # Move file to captures
            os.rename(capture.tmp_filepath, capture.dest_filepath)

        except Exception as exception:
            self.log.error(f'Exception in CapturesProcessor: {exception}')


    def build_template(self, src, width, height):
        return "<!DOCTYPE html>" \
               "<html lang=\"en\">" \
               "<head>" \
               " <meta charset=\"UTF-8\">" \
               " <title>Title</title>" \
               "</head>" \
               "<body>" \
               "<iframe src={src} width={width} height={height} frameborder='0' scrolling='no' marginwidth='0'>" \
               "</iframe>" \
               "</body>" \
               "</html>".format(src=src, width=width, height=height)