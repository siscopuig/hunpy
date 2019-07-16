import requests
import aiohttp
from asyncio import TimeoutError
from aiohttp import ClientError
from hunpy.log import Log



class UtilsRequest:


    def __init__(self, bad_http, headers):

        self.log = Log()
        self.bad_http = bad_http
        self.headers = headers

    def get_http_response(self, src):

        response = {
            "url": src,
            "finfo": "",
            "request": "",
            "valid": False
        }

        try:
            r = requests.get(src, timeout=3, headers=self.headers)

            if r.status_code in self.bad_http:
                self.log.debug(f'http error: {r.status_code}')
                return False

            if len(r.text) < 100:
                self.log.debug(f'Response text (html body) is empty for origin source: {src}')
                return False

            effective_url = self.get_effective_url(r)
            if effective_url is not None:
                response['url'] = effective_url
            else:
                response['url'] = src

            finfo = r.headers['Content-Type']
            if 'text/html' in finfo and len(finfo) > 9:
                finfo = finfo[:9]

            response['request'] = r
            response['finfo'] = finfo
            response['valid'] = True

            return response

        except requests.exceptions.Timeout:
            self.log.debug(f'Request Exception Timeout, src: ({src})')

        except requests.exceptions.TooManyRedirects:
            self.log.debug(f'Request Exception TooManyRedirects, src: ({src})')

        except requests.exceptions.RequestException:
            self.log.debug(f'Request Exception , src: ({src})')

        return False


    def get_effective_url(self, response, effective_url=None):

        # For debugging purposes
        if response.history:
            self.log.debug('Request was redirected')

            for resp in response.history:
                self.log.debug(f'Status code: {resp.status_code}, url: {resp.url}')

                if resp.status_code == 200:
                    effective_url = resp.url

            self.log.debug(f'Final destination, status {response.status_code} final url: {effective_url}')

        return effective_url


    async def process_http_requests(self, items):

        for i, item in enumerate(items):
            try:
                async with aiohttp.ClientSession(conn_timeout=5) as session:
                    async with session.get(item.img_src, timeout=5, headers=self.headers) as resp:
                        item.request['status'] = resp.status
                        item.request['content_type'] = resp.content_type
            except TimeoutError as e:
                print(e)
            except ClientError as e:
                print(e)


###########################################################################
# src = 'https://s0.2mdn.net/ads/richmedia/studio/pv2/60804105/index.html'
# get_http_request(src)
# bad_requests = [0, 400, 404]
# request = {"status": 0, "content_type": ""}
# src_0 = 'http://ds.serving-sys.com/resources///PROD/asset/43572/IMAGE/20180907/103777_WATER_CBI_728x90_v1_39469178948688286_39662342314662580.jpg'
#src1 = 'https://s0.2mdn.net/ads/richmedia/studio/pv2/60804105/20180829074403650/index.html?e=69&amp;renderingType=2&amp;leftOffset=0&amp;topOffset=0&amp;c=W8zfXE0qnC&amp;t=1'
#src2 = 'http://localhost:63342/hunpy/lab/html_templates/html_main_document.html'
# is_invalid_http_request(src_0, bad_requests, request)
#request_src(src1)
#request_src(src2)

