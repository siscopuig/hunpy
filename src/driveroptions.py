
from selenium.webdriver.chrome.options import Options

#TODO get config values from yaml file

class DriverOptions:


	def __init__(self):

		self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
						  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64_59.0.3071.86 Safari/537.36'
		self.prefs = {
			'profile.default_content_setting_values.notifications': 2
		}


		self.chrome_options = Options()
		self.chrome_options.add_argument('--user-data-dir=/home/sisco/PycharmProjects/hunpy/profile')
		self.chrome_options.add_argument('--window-size=1366x768')
		self.chrome_options.add_argument('--user-agent=' + self.user_agent)
		self.chrome_options.add_argument('--ignore-ssl-errors=true')
		#self.chrome_options.add_argument('--headless')

		# self.chrome_options.arguments(
		# 	'--window-size=1366x768',
		# 	'--user-agent=' + self.user_agent,
		# 	'--ignore-certificate-errors',
		# 	'--ignore-ssl-errors=true',
		# 	'--dns-prefetch-disable',
		# 	'--disable-infobars',
		# 	'--disable-session-crashed-bubble',
		# 	'--disable-notifications',
		# 	'--no-sandbox',
		# 	#'--headless',
		# 	#'--disable-gpu',
		# )

		self.chrome_options.add_experimental_option(
			'prefs',self.prefs
		)

