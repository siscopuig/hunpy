import pymysql
from pymysql import MySQLError


class MsqlConn:

	def __init__(self):

		self.conn = None
		self.connect_params = {
			'user': 'root',
			'password': 'pupahit66',
			'host': 'localhost',
			'database': 'dfa_urls'
		}


	def connect(self):

		try:
			if self.conn is None:
				self.conn = pymysql.connect(**self.connect_params)
		except MySQLError as e:
			print(e)
			self.conn = None


	def select_urls(self):
		sql = "SELECT u_id, target, qualifier, audience, u_url, cycles_limit, status FROM Urls"
		cursor = self.conn.cursor()
		return cursor.execute(sql, )
		pass


	# def select(self, url):
	#
	# 	sql = "SELECT url FROM Urls where url =%s"
	# 	cursor = self.conn.cursor()
	# 	result = cursor.execute(sql, (url,))
	# 	if result:
	# 		return True
	# 	else:
	# 		return False


	# def insert(self, url):
	#
	# 	sql = "INSERT INTO `Urls` (url) VALUES (%s)"
	# 	cursor = self.conn.cursor()
	# 	cursor.execute(sql, (url,))
	# 	self.conn.commit()


	def close(self):

		if self.conn:
			self.conn.close()
			self.conn = None
