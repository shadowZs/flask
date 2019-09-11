from flask_cors import CORS
from flask import Flask, Response, jsonify, request
from models import insert_user, create_user_table


app = Flask(__name__)

create_user_table()

@app.route("/login", methods=['POST'])
def login():
	return jsonify({'code': 1, 'message': '登录成功', 'data':'1111'})


@app.route('/register', methods= ['POST'])
def register():
	mobile = request.form.get['mobile']
	password = request.form.get['password']
	nick_name = request.form.get['nickName']
	print(mobile, password, nick_name)
	insert_user(mobile, password, nick_name)
	
	return jsonify({'code': 1, 'message': '注册成功', 'data': '注册成功'})


if __name__ == "__main__":
	CORS(app, supports_credentials=True)
	app.run()
