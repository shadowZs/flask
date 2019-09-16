from flask_cors import CORS
from flask import Flask, Response, jsonify, request, url_for, redirect, session
from werkzeug import secure_filename   # 用来对文件名进行安全监测
import json
from models import DBManager
import os

# static_url_path  static_folder 配置静态资源文件夹
app = Flask(__name__, static_url_path='/static')
app.config['base_host'] = 'http://localhost:5000'

DBManager().create_user_table()
DBManager().create_article_list()

# form 表单提交可以通过 request.form.get() / form[] 来获取参数
# post 非表单提交可以通过 request.get_data 来获取,
# json.loads(s)  json解码 （json.load 是用来处理文件） json.dumps() json 编码


# session 登录验证
# def wrapper(func):


# 登录
@app.route("/login", methods=['POST'])
def login():
	data = request.get_data()
	res = json.loads(data)
	print('data:', res)
	mobile = res['mobile']
	password = res['password']
	result = DBManager().get_user_by_mobile(mobile)
	print('result:', result)
	if result['password'] == password:
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
	return jsonify({'code': 1, 'message': '注册成功', 'data': '注册成功'})


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
	
	
if __name__ == "__main__":
	app.config['JSON_AS_ASCII'] = False    # 解决返回值中文乱码
	CORS(app, supports_credentials=True)
	app.run()

# 添加文章
@app.route('/addArticle', methods=['POST', 'GET'])
def add_article():
	if request.method == 'POST':
		data = request.get_data()
		req = json.loads(data)
		_id = req['id']
		title = req['title']
		content = req['content']
		_userInfo = DBManager().get_user_by_id(_id)
		print('userInfo:', _userInfo)
		
