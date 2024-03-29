from flask_cors import CORS
from flask import Flask, Response, jsonify, request, url_for, redirect, session
from werkzeug import secure_filename   # 用来对文件名进行安全监测
import json
from datetime import timedelta
import datetime
from models import DBManager
import os
from urllib.request import quote, unquote

# static_url_path  static_folder 配置静态资源文件夹
app = Flask(__name__, static_url_path='/static')
app.config['base_host'] = 'http://localhost:5000'

DBManager().create_user_table()
DBManager().create_article_list()
DBManager().create_article_type()

# form 表单提交可以通过 request.form.get() / form[] 来获取参数
# post 非表单提交可以通过 request.get_data 来获取,
# json.loads(s)  json解码 （json.load 是用来处理文件） json.dumps() json 编码


# session 登录验证
# def wrapper(func):

# flask cookie 操作
# 设置cookie response.set_cookie(key, value, expires)
# 获取cookie  request.cookies.get(key)
# 删除cookie response.delete_cookie(key)

# session 操作 一般用户检查登录状态 与flask_session 的区别
app.config['SECRECT_KEY'] = os.urandom(24)   # 返回24个字节的字符串
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)   # 设置session的保存时间
#
# # session 设置、获取、删除
# session['x'] = 'x'
# session.pop('x')
# session.clear()   # 删除全部


# def login_required(func):
# 	# 检查登录状态
# 	@wraps(func)
# 	def wrapper(*args, **kwargs):
# 		user_id = session.get('user_id')
# 		if user_id is not None:
# 			g.user_id = user_id
# 			return func(*args, **kwargs)
# 		else:
# 			return jsonify({'code': 488, 'message': '用户未登录'})
# 	return wrapper


# 登录
@app.route("/login", methods=['POST'])
def login():
	data = request.get_data()
	res = json.loads(data)
	print('data:', res)
	mobile = res['mobile']
	password = res['password']
	result = DBManager().get_user_by_mobile(mobile)
	print('result:', result, result['password'] == password)
	if result and result['password'] == password:
		return jsonify({'code': 1, 'message': '登录成功', 'data': result})
	else:
		return jsonify({'code': 0, 'message': '账号密码错误', 'data': '账号密码错误'})

# 注册
@app.route('/register', methods=['POST'])
def register():
	data = request.get_data()
	res = json.loads(data)
	mobile = res['mobile']
	password = res['password']
	nick_name = res['nickName']
	print(mobile, password, nick_name)
	_result = DBManager().insert_user(mobile, password, nick_name)
	print('result:', _result)
	return jsonify({'code': 1, 'message': '注册成功', 'data': _result})


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
	
# 上传文件 os模块处理文件相关  os.path.join() 路径拼接
@app.route('/upload', methods=['POST', 'GET'])
def upload():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			file.save(os.path.join(os.path.join(os.getcwd()), 'static', file.filename))
			file_url = os.path.join(os.path.join(app.config['base_host']), 'static', file.filename)
			print('file_url:', file_url);
			return jsonify({'code': 1, 'message': '上传成功', 'data': file_url})
	
# 添加文章
@app.route('/addArticle', methods=['POST'])
def add_article():
	if request.method == 'POST':
		data = request.get_data()
		req = json.loads(data)
		_id = req['userId']
		title = req['title']
		content = req['content']
		_userInfo = DBManager().get_user_by_id(_id)
		_author = _userInfo['nick_name']
		_create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		_result = DBManager().insert_article(title, content, _create_time, _author, _id)
		print('result:', _result)
		return jsonify({'code': 1, 'data': '保存成功', 'message': '保存成功'})


# 文章标签
@app.route('/articleTypes', methods=['GET'])
def article_types():
	if request.method == 'GET':
		_result = DBManager().get_article_type()
		return jsonify({'code': 1, 'data': _result, 'message': '成功'})

# 文章列表
# String '0': 默认排序
# String '1': 热门排序
@app.route('/articleList', methods=['GET'])
def article_list():
	if request.method == 'GET':
		page_no = int(request.args.get('pageNo'))   # page_no, page_size 为整形，str操作数据库会报错
		page_size = int(request.args.get('pageSize'))
		_type = request.args.get('type')
		
		if _type == '0':
			_result = DBManager().get_article_list(None, page_no, page_size)
			return jsonify({'code': 1, 'data': _result, 'message': '获取文章里列表成功'})
		
		elif _type == '1':
			_result = DBManager().get_article_list_hot()
			return jsonify({'code': 1, 'data': _result, 'message': '获取文章里列表成功'})
			
		else:
			cookies = request.cookies.get('blog_user')    # 获取cookie 会自动编码？
			if cookies is None:
				return jsonify({'code': 0, 'data': '请登录', 'message': '未登录状态，请重新登录'})
			else:
				cookies = json.loads(unquote(cookies))
				_id = cookies['id']
				if _id is None:
					return jsonify({'code': 0, 'data': '请登录', 'message': '未登录状态，请重新登录'})
				else:
					_result = DBManager().get_article_list(_id)
					return jsonify({'code': 1, 'data': _result, 'message': '获取文章里列表成功'})
		

# 我发表的文章
@app.route('/articleListByUser', methods=['GET'])
def article_list_by_user():
	if request.method == 'GET':
		user_id = request.args.get('id')
		print(1111111, request.args.get('pageNo'))
		page_no = int(request.args.get('pageNo'))
		page_size = int(request.args.get('pageSize'))
		print('我发表的文章：', user_id, page_no, page_size)
		if user_id is None:
			return jsonify({'code': 0, 'data': '', 'message': '请登录'})
		else:
		
			_result = DBManager().get_article_list_by_user(user_id)
			print('我的文章：', _result)
			return jsonify({'code': 1, 'data': _result, 'message': '获取我的文章列表成功'})

# 文章详情
@app.route('/articleDetail', methods=['GET'])
def article_detail():
	if request.method == 'GET':
		_id = request.args.get('id')
		_result = DBManager().get_article_detail(_id)
		print('result:', _result)
		return jsonify({'code': 1, 'data': _result, 'message': '获取文章详情成功'})
	
	
if __name__ == "__main__":
	app.config['JSON_AS_ASCII'] = False    # 解决返回值中文乱码
	CORS(app, supports_credentials=True)
	app.run()
