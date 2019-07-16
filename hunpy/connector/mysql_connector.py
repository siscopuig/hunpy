# -*- coding: utf-8 -*-

import pymysql.cursors
from pymysql import MySQLError
from hunpy.log import Log


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
	def select_placements(self):
		sql = "SELECT width, height FROM Placements"
		self.cursor.execute(sql)
		return self.cursor.fetchall()


	@ewe
	def insert_new_advert(self, data):

		sql = "INSERT INTO Adverts (" \
			  "uid, advertiser, src, width, height, landing, finfo, isframe, x, y)" \
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


