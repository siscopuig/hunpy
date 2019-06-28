import os
import io
import requests
from PIL import Image
from hunpy.log import Log
from hunpy.processor import Processor
from hunpy.utils.utils_date import UtilsDate

# @TODO Do not process same image twice
# @TODO Put constant var in config file if possible

class CapturesProcessor(Processor):

    batch = []

    WORKING_DIR = '/home/sisco/Sites/python/hunpy'
    LOCALHOST_TMPL_PATH = 'http://0.0.0.0:8080/html_template.html'
    TMPL_PATH = '/home/sisco/Workspace/Docker/nginx/html/html_template.html'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/75.0.3770.90 Safari/537.36'
    }

    def __init__(self, driver, config, datasource):
        super().__init__(driver, config, datasource)
        self.driver = driver
        self.log = Log()


    def process(self, page):

        if page.adverts:
            self.extract_process_list(page)

        for advert in self.batch:

            if advert['type'] == 'static':
                self.process_static(advert)

            if advert['type'] == 'dynamic':
                self.process_dynamic(advert)


    def process_dynamic(self, advert):

        try:

            if not os.path.exists(advert['dest_path']):
                os.makedirs(advert['dest_path'])

            # Truncate file (delete content)
            with open(self.TMPL_PATH, 'w') as f:
                f.truncate(0)

            # Write html content in file
            html_template = self.build_template(advert['src'], advert['width'], advert['height'])
            with open(self.TMPL_PATH, 'w') as f:
                f.write(html_template)

            self.driver.open('http://0.0.0.0:8080/html_template.html', 3)

            # Get iframe position
            element = self.driver.find_elements_by_xpath('//iframe')
            pos = dict()
            pos['x'] = element[0].rect['x']
            pos['y'] = element[0].rect['y']

            self.driver.save_screenshot(advert['tmp_filepath'])
            image = Image.open(io.FileIO(advert['tmp_filepath']))
            image = image.crop((int(pos['x']), int(pos['y']), int(advert['width']), int(advert['height'])))
            image_rgb = image.convert('RGB')
            image_rgb.save(advert['dest_filepath'], format('JPEG'))

            # Remove file
            os.remove(advert['tmp_filepath'])

        except Exception as exception:
            self.log.error(f'Exception on CapturesProcessor::process_dynamic()\n {exception}')


    def process_static(self, advert):

        try:

            r = requests.get(advert['src'], headers=self.HEADERS)
            if r.status_code is not 200:
                self.log.warning(f"error status code {r.status_code}")
                return False

            # @TODO Perform a validation with file info image list
            finfo = r.headers['Content-Type']
            if finfo != advert['finfo']:
                self.log.warning(f"Stored file info: {advert['finfo']} not equal to {finfo}")
                return False

            # Save img on tmp dir
            with Image.open(io.BytesIO(r.content)) as img:
                img.save(advert['tmp_filepath'])

            # Create path in captures
            if not os.path.exists(advert['dest_path']):
                os.makedirs(advert['dest_path'])

            # Move file to captures
            os.rename(advert['tmp_filepath'], advert['dest_filepath'])

        except Exception as exception:
            self.log.error(f'Exception on CapturesProcessor::process_static()\n {exception}')


    def extract_process_list(self, page):

        for i, advert in enumerate(page.adverts):

            cap = dict()
            cap['uuid'] = advert.uid
            cap['src'] = advert.src
            cap['width'] = advert.size[0]
            cap['height'] = advert.size[1]
            cap['finfo'] = advert.finfo

            uuid = advert.uid
            date = UtilsDate.get_date()
            dest_base_path = '/'.join([self.WORKING_DIR, 'captures/store', date])

            if not advert.finfo == 'text/html':
                cap['type'] = 'static'
                finfo = advert.finfo
                cap['ext'] = finfo.split('/')[1]
                cap['filename'] = '.'.join([uuid, cap['ext']])
                cap['tmp_filepath'] = '/'.join([self.WORKING_DIR, 'captures/tmp', cap['filename']])
                cap['dest_path'] = dest_base_path
                cap['dest_filepath'] = dest_base_path + '/' + cap['filename']

            else:
                cap['type'] = 'dynamic'
                cap['filename'] = '.'.join([uuid, 'jpeg'])
                cap['tmp_filepath'] = self.WORKING_DIR + '/captures/tmp/' + uuid + '.png'
                cap['dest_path'] = dest_base_path
                cap['dest_filepath'] = dest_base_path + '/' + cap['filename']

            self.log.debug(cap)

            self.batch.append(cap)


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
