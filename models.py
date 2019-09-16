import pymysql


# connection.cursor(pymysql.cursors.DictCursor) 增加该设置会返回字典，不设置返回元祖

class DBManager(object):
	# init 初始化会在对象创建后立即执行
	def __init__(self):
		self.connection = pymysql.connect(
			host='localhost',
			user='root',
			password='root',
			db='blog',
			charset='utf8mb4',
		)
		
	def create_user_table(self):
		try:
			with self.connection.cursor() as cursor:
				_sql = "CREATE TABLE IF NOT EXISTS users(" \
					   "id int(11) NOT NULL AUTO_INCREMENT, " \
					   "mobile varchar(30) NOT NULL," \
					   "password varchar(20) NOT NULL," \
					   "nick_name varchar(30) NOT NULL,PRIMARY KEY(id)) ENGINE=InnoDB COLLATE=utf8_bin"
				cursor.execute(_sql)
				self.connection.commit()

		finally:
			self.connection.close()
	
	# 创建文章列表表
	def create_article_list(self):
		try:
			with self.connection.cursor() as cursor:
				_sql = "CREATE TABLE IF NOT EXISTS article_list(" \
					   "id int(11) NOT NULL AUTO_INCREMENT," \
					   "title varchar(30) NOT NULL," \
					   "content varchar(1000) NOT NULL," \
					   "create_time datetime NOT NULL," \
					   "update_time datetime," \
					   "likes int(10) NOT NULL," \
					   "dislikes int(10) NOT NULL," \
					   "author varchar(10) NOT NULL, " \
					   "PRIMARY KEY(id))ENGINE=InnoDB COLLATE=utf8_bin"
				cursor.execute(_sql)
				self.connection.commit()
		finally:
			self.connection.close()
	
	# 添加用户
	def insert_user(self, mobile, password, nick_name):
		try:
			with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
				_sql = "INSERT INTO users (mobile, password, nick_name) VALUES (%s, %s, %s)"
				cursor.execute(_sql, mobile, password, nick_name)
				self.connection.commit()

		finally:
			self.connection.close()

	# 通过手机号查询用户信息 fetchone() 返回一条数据， fetchall() 返回多个数据, fetchmany
	def get_user_by_mobile(self, mobile):
		try:
			with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
				_sql = "SELECT * FROM users WHERE mobile = %s"
				cursor.execute(_sql, mobile)
				result = cursor.fetchone()
				print('result1:', result)
				self.connection.commit()
				return result
		finally:
			self.connection.close()

	# 通过id查询用户信息
	def get_user_by_id(self, _id):
		try:
			with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
				_sql = "SELECT * FROM users WHERE id = %s"
				cursor.execute(_sql, _id)
				result = cursor.fetchone()
				print('result1:', result)
				self.connection.commit()
				return result
		finally:
			self.connection.close()

	# 插入文章
	def insert_article(self,_id, _title, _content, _author, _author_id):
		try:
			with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
				_sql = "INSET INTO article_list(title, content, create_time, update_time, likes, dislikes, author, author_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
				_create_time = ''
				_update_time = ''
				_likes = 0
				_dislikes = 0
				cursor.execute(_sql, _title, _content, _create_time, _update_time, _likes, _dislikes, _author, _author_id)
				self.connection.commit()
			
		finally:
			self.connection.close()
