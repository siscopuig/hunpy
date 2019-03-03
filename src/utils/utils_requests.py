import requests
import aiohttp
from asyncio import TimeoutError
from aiohttp import ClientError


HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'}


async def process_http_requests(items):

	for i, item in enumerate(items):

		try:

			async with aiohttp.ClientSession(conn_timeout=5) as session:
				async with session.get(item.img_src, timeout=5, headers=HEADERS) as resp:
					item.request['status'] = resp.status
					item.request['content_type'] = resp.content_type

		except TimeoutError as e:
			print(e)

		except ClientError as e:
			print(e)


def get_http_request(src):

	# if is_invalid_status(request['status'], http_bad_request):
	# 	print('Invalid response: {} for src: {}'.format(status=status, src=src))
	# 	return True
	# else:
	# 	print('Valid response: {status} for src: {src}'.format(status=status, src=src))
	# 	return False

	try:
		request = {}
		r = requests.get(src)
		request['status'] = r.status_code
		request['content_type']  = r.headers.__getitem__('Content-Type')
		return request

	except Exception as e:
		print(e)
		return False





















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

