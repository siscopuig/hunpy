import pymysql.cursors
from pymysql import MySQLError
from log import Log

# https://pymysql.readthedocs.io/en/latest/index.html
# https://pymysql.readthedocs.io/en/latest/user/examples.html

# PyMySQL is a pure Python (no C low-level code) implementation that
# attempts to be a drop-in replacement for MySQLdb. However, some MySQL
# APIs are not supported by the driver so whether or not your application
# can use this connector will depend on what you're building.


def ewe(func):

	def wrapper(self, *args, **kwargs):

		try:

			result = func(self, *args, **kwargs)

			if not result:
				return []

			return result

		except MySQLError as exception:
			self.log.error('PyMySQL error {}'.format(exception))

	return wrapper


class MysqlConn:


	def __init__(self, conn_param):

		self.log = Log()

		self.conn = None

		self.cursor = None

		self.conn_param = conn_param

		if 'charset' not in self.conn_param:
			self.conn_param['charset'] = 'utf8mb4'

		if 'cursorclass' not in self.conn_param:
			self.conn_param['cursorclass'] = pymysql.cursors.DictCursor


	@ewe
	def connect(self):

		if self.conn is None:

			try:
				self.conn = pymysql.connect(**self.conn_param)
				self.cursor = self.conn.cursor()

			except MySQLError as exception:
				self.conn = None
				raise exception

	@ewe
	def close(self):
		if self.conn:
			self.conn.close()
			self.conn = None


	@ewe
	def select_urls(self):
		sql = "SELECT id, url FROM Urls"
		self.cursor.execute(sql)
		return self.cursor.fetchall()


	@ewe
	def select_adservers(self):
		sql = "SELECT domain FROM Adservers"
		self.cursor.execute(sql)
		return self.cursor.fetchall()


	@ewe
	def select_placements(self):
		sql = "SELECT width, height FROM Placements"
		self.cursor.execute(sql)
		return self.cursor.fetchall()


	@ewe
	def insert(self, url):
		sql = "INSERT INTO Urls (url) VALUES (%s)"
		self.cursor.execute(sql, (url,))
		self.conn.commit()


	@ewe
	def select_from_where_equal_to(self, col, table, item, value):
		sql = "SELECT {col} FROM {table} WHERE {item} = %s".format(col=col, table=table, item=item)
		self.cursor.execute(sql, (value,))
		return self.cursor.fetchall()


	@ewe
	def select_instance_record_by_date(self, id, table, uid,  url_id, date):
		sql = "SELECT {id} FROM {table} WHERE uid = %s " \
			  "AND url_id = %s AND `date` = %s".format(
			id=id, table=table, uid='uid', url_id=url_id, date=date)
		self.cursor.execute(sql, (uid, url_id, date))
		return self.cursor.fetchall()


	@ewe
	def insert_new_instance_record(self, uid, url_id, counter, date):
		sql = "INSERT INTO Instances (uid, url_id, counter, date) " \
			  "VALUES (%s, %s, %s, %s)"
		self.cursor.execute(sql, (uid, url_id, counter, date))
		self.conn.commit()


	@ewe
	def update_existing_instance_record(self, id, date, instances):
		sql = "UPDATE Instances SET counter = counter + {instances} WHERE id = %s " \
			  "AND `date` = %s".format(instances=instances)
		self.cursor.execute(sql, (id, date))
		self.conn.commit()



	@ewe
	def insert_new_advert(self, data):

		sql = "INSERT INTO Adverts (" \
			  "uid, advertiser, src, width, height, landing, finfo, isframe, x, y) " \
			  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		cursor = self.conn.cursor()
		cursor.execute(sql, (
			data['uid'],
			data['advertiser'],
			data['src'],
			data['width'],
			data['height'],
			data['landing'],
			data['finfo'],
			data['isframe'],
			data['x'],
			data['y']))
		self.conn.commit()


	@ewe
	def select_existing_source(self, source):
		"""
		This query will return a dict instead of a tuple of tuples
		:param source:
		:return: a dict list
		"""
		sql = "SELECT id, uid, advertiser FROM Adverts WHERE src = %s"
		self.cursor.execute(sql, (source,))
		return self.cursor.fetchall()


	@ewe
	def today_new_cycle(self, url_id, date):

		sql = "SELECT id FROM Cycles WHERE url_id = %s AND date = %s"
		self.cursor.execute(sql, (url_id, date))
		return self.cursor.fetchall()

	@ewe
	def insert_cycle(self, url_id, cycles, date):

		sql = "INSERT INTO Cycles (url_id, cycles, date) VALUES (%s, %s, %s)"
		self.cursor.execute(sql, (url_id, cycles, date))
		self.conn.commit()


	@ewe
	def update_cycle(self, id, date):

		sql = "UPDATE Cycles SET cycles = cycles + 1 " \
			  "WHERE id = %s AND date = %s LIMIT 1"
		self.cursor.execute(sql, (id, date))
		self.conn.commit()