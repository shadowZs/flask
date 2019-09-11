import pymysql

config = {
	'host': 'localhost',
	'user': 'root',
	'password': 'root',
	'port': 3306,
	'db': 'blog'
}

connection = pymysql.connect(
	host='localhost',
	user='root',
	password='root',
	db='blog',
	charset='utf8mb4',
)


def create_user_table():
	try:
		with connection.cursor() as cursor:   #返回一个指针对象，用于访问和操作数据库中的数据
			_sql = "CREATE TABLE IF NOT EXISTS `users`("\
				   "`id` int(11) NOT NULL AUTO_INCREMENT)",\
				   "`mobile` varchar(30) NOT NULL",\
				   "`password` varchar(20) NOT NULL",\
				   "`nick_name` varchar(30) NOT NULL",\
				   "PRIMARY KEY(`id`)" \
				   ")ENGINE=InnoDB DEFAULT=uft8 COLLATE=utf8_bin"
			cursor.execute(_sql)
			connection.commit()
			
	finally:
		connection.close()


def insert_user(mobile, password, nick_name):
	try:
		with connection.cursor() as cursor:
			_sql = "INSERT INTO `users` (`mobile, `password`, `nick_name`) VALUES (mobile, password, nick_name)"
			cursor.execute(_sql)
			connection.commit()
		
	finally:
		connection.close()

