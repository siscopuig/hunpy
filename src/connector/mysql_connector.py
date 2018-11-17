import pymysql.cursors
from pymysql import MySQLError
from src.log import Log
# https://pymysql.readthedocs.io/en/latest/index.html



def ewe(func):

	def wrapper(self, *args, **kwargs):

		try:

			result = func(self, *args, **kwargs)

			if not result:
				return []

			return result

		except MySQLError as e:
			# (1406, "Data too long for column 'landing' at row 1")
			print('MySQL Error: '.format(e))

	return wrapper


class MysqlConn:


	# @todo:
	# If all the data from database is accessed from
	# class data manager there is no point to implement
	# a Singleton pattern


	# connect_params = {
	# 	'user': 'root',
	# 	'password': 'pupahit66',
	# 	'host': 'localhost',
	# 	'database': 'hunpy'
	# }



	def __init__(self, conn_param):

		self.log = Log
		self.cursor = ''
		self.conn = pymysql.connect(**conn_param)


	@ewe
	def select_urls(self):
		sql = "SELECT id, url FROM Urls"
		cursor = self.conn.cursor()
		cursor.execute(sql)
		return cursor.fetchall()


	@ewe
	def select_adservers(self):
		sql = "SELECT domain FROM Adservers"
		cursor = self.conn.cursor()
		cursor.execute(sql)
		return cursor.fetchall()


	@ewe
	def select_placements(self):
		sql = "SELECT width, height FROM Placements"
		cursor = self.conn.cursor()
		cursor.execute(sql)
		return cursor.fetchall()


	@ewe
	def close(self):
		if self.conn:
			self.conn.close()
			self.conn = None


	@ewe
	def insert(self, url):
		sql = "INSERT INTO Urls (url) VALUES (%s)"
		cursor = self.conn.cursor()
		cursor.execute(sql, (url,))
		self.conn.commit()


	@ewe
	def select_from_where_equal_to(self, col, table, item, value):
		sql = "SELECT {col} FROM {table} WHERE {item} = %s".format(col=col, table=table, item=item)
		cursor = self.conn.cursor()
		cursor.execute(sql, (value,))
		return cursor.fetchall()


	@ewe
	def select_instance_record_by_date(self, id, table, uid,  url_id, date):
		sql = "SELECT {id} FROM {table} WHERE uid = %s " \
			  "AND url_id = %s AND `date` = %s".format(
			id=id, table=table, uid='uid', url_id=url_id, date=date)
		cursor = self.conn.cursor()
		cursor.execute(sql, (uid, url_id, date))
		return cursor.fetchall()


	@ewe
	def insert_new_instance_record(self, uid, url_id, counter, date):
		sql = "INSERT INTO Instances (uid, url_id, counter, date) " \
			  "VALUES (%s, %s, %s, %s)"
		cursor = self.conn.cursor()
		cursor.execute(sql, (uid, url_id, counter, date))
		self.conn.commit()


	@ewe
	def update_existing_instance_record(self, id, date, instances):
		sql = "UPDATE Instances SET counter = counter + {instances} WHERE id = %s " \
			  "AND `date` = %s".format(instances=instances)
		cursor = self.conn.cursor()
		cursor.execute(sql, (id, date))
		self.conn.commit()
		print(0)


	@ewe
	def insert_new_advert(self, advert):

		src = advert.src
		uid = advert.uid
		width = advert.width
		height = advert.height
		landing = advert.landing
		advertiser = advert.advertiser
		finfo = advert.finfo
		isframe = advert.is_iframe


		sql = "INSERT INTO Adverts (" \
			  "uid, advertiser, src, width, height, landing, finfo, isframe) " \
			  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
		cursor = self.conn.cursor()
		cursor.execute(sql, (uid, advertiser, src, width, height, landing, finfo, isframe))
		self.conn.commit()


	@ewe
	def select_existing_source(self, source):
		"""
		This query will return a dict instead of a tuple of tuples
		:param source:
		:return: a dict list
		"""
		sql = "SELECT id, uid, advertiser FROM Adverts WHERE src = %s"
		cursor = self.conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(sql, (source,))
		return cursor.fetchall()


###############################################################

# connect_params = {
# 	'user': 'root',
# 	'password': 'pupahit66',
# 	'host': 'localhost',
# 	'database': 'hunpy'
# }
# 
# src = 'https://tpc.googlesyndication.com/simgad/2143365295016291254'
# 
# conn = MysqlConn(connect_params)
# 
# result = conn.select_existing_source(src)
# 
# print(result)
# if len(result) >= 2:
# 	print(len(result))
# 
# print(result[0])
# 
# 
# if result[0]['id']:
# 	print(result[0]['id'])




# result = foo.select_from_where('http://ds.serving-sys.com/resources/PROD/asse'
# 							   't/43572/IMAGE/20180110/MEETING_CBI17_728x90_34113136763077999.jpg')

# result = (('https://tpc.googlesyndication.com/simgad/4812493872611183408'),
# 		  ('https://tpc.googlesyndication.com/simgad/4812493872611183408'))
#
# for x in result:
# 	print(

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

