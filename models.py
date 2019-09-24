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
					   "update_time datetime DEFAULT NULL," \
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
				print('通过id查询用户信息:', result, _id)
				self.connection.commit()
				return result
		finally:
			self.connection.close()

	# 插入文章
	def insert_article(self, _title, _content, _create_time, _author, _id):
		try:
			with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
				print(1)
				_sql = "INSERT INTO article_list(title, content, create_time, likes, dislikes, author, author_id) VALUES(%s, %s, %s, %s, %s, %s, %s)"
	
				_likes = 0
				_dislikes = 0
				print('++++++++++++++',)
				cursor.execute(_sql, (_title, _content, _create_time, _likes, _dislikes, _author, _id))
				self.connection.commit()
		finally:
			self.connection.close()
	
	# 文章列表
	def get_article_list(self, _id, page_no, page_size):
		try:
			with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
				if _id is not None:
					_sql = "SELECT * FROM article_list WHERE author_id = %s limit 1, 10"
					cursor.execute(_sql, _id)
				else:
					_sql = "SELECT * FROM  article_list limit %s,%s"
					print('page_no:', page_no, type(page_no))
					cursor.execute(_sql, (page_no, page_size))
				
				result = cursor.fetchall()
				self.connection.commit()
				return result
		finally:
			self.connection.close()
			
	# 热门文章列表
	def get_article_list_hot(self):
		try:
			with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
				_sql = "SELECT * FROM article_list"
				cursor.execute(_sql)
				result = cursor.fetchall()
				self.connection.commit()
				return result
		finally:
			self.connection.close()
	
	# 根据id查询文章详情
	def get_article_detail(self, _id):
		try:
			with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
				_sql = "SELECT * FROM article_list WHERE id = %s"
				cursor.execute(_sql, _id)
				result = cursor.fetchone()
				self.connection.commit()
				return result
		finally:
			self.connection.close()
