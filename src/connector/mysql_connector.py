import pymysql.cursors
from pymysql import MySQLError
import sys

# https://pymysql.readthedocs.io/en/latest/index.html



def ewe(func):

	def wrapper(self, *args, **kwargs):
		try:
			func(self, *args, **kwargs)
		except Exception as e:
			# (1406, "Data too long for column 'landing' at row 1")
			print(e)
	return wrapper

class MysqlConn:

	"""
	Singleton implementation.
	"""
	connect_params = {
		'user': 'root',
		'password': 'pupahit66',
		'host': 'localhost',
		'database': 'hunpy'
	}

	instance = None
	conn = ''
	cursor = None


	def __new__(cls):

		if cls.instance is None:
			cls.instance = super().__new__(cls)
			try:
				if cls.conn is not None:
					cls.conn = pymysql.connect(**cls.connect_params)
			except MySQLError as e:
				sys.exit(e)

		return cls.instance



	def select_urls(self):
		sql = "SELECT id, url FROM Urls"
		cursor = self.conn.cursor()
		cursor.execute(sql)
		return cursor.fetchall()


	def select_adservers(self):
		sql = "SELECT domain FROM Adservers"
		cursor = self.conn.cursor()
		cursor.execute(sql)
		return cursor.fetchall()


	def select_placements(self):
		sql = "SELECT width, height FROM Placements"
		cursor = self.conn.cursor()
		cursor.execute(sql)
		return cursor.fetchall()


	def close(self):
		if self.conn:
			self.conn.close()
			self.conn = None


	def insert(self, url):
		sql = "INSERT INTO Urls (url) VALUES (%s)"
		cursor = self.conn.cursor()
		cursor.execute(sql, (url,))
		self.conn.commit()


	@ewe
	def insert_advert(self, advert):

		uid = advert.uid
		advertiser = advert.advertiser
		src = advert.src
		width = advert.width
		height = advert.height
		landing = advert.landing
		finfo = advert.finfo

		#print('stop')

		sql = "INSERT INTO Adverts (" \
			  "uid, advertiser, src, width, height, landing, finfo) " \
			  "VALUES (%s, %s, %s, %s, %s, %s, %s)"
		cursor = self.conn.cursor()
		cursor.execute(sql, (uid, advertiser, src, width, height, landing, finfo))
		self.conn.commit()

###############################################################
# foo = MysqlConn()
# advert = {
# 	'uid': 'fdkhfksjhfjdshfksdjhf',
# 	'advertiser': 'jupiter.com',
# 	'src': 'https://tpc.googlesyndication.com/simgad/4812493872611183408',
# 	'width': '150',
# 	'height': '90',
# 	'landing': 'https://www4.troweprice.com/gis/tpd/dk/en/home.html',
# 	'finfo': 'text/html'
# }
# foo.insert_advert(advert)

# result = foo.select_urls()
# for id, url in result:
# 	print('id: {} url: {}'.format(id, url))
#
# foo1 = MysqlConn()
# result2 = foo1.select_ad_servers()
# for id, domain in result2:
# 	print('id: {} domain: {}'.format(id, domain))

		# for key, value in advert.items():
		# 	if key == 'uid':
		# 		uid = value
		# 	if key == 'advertiser':
		# 		advertiser = value
		# 	if key == 'src':
		# 		src = value
		# 	if key == 'width':
		# 		width = value
		# 	if key == 'height':
		# 		height = value
		# 	if key == 'landing':
		# 		landing = value
		# 	if key == 'finfo':
		# 		finfo = value

