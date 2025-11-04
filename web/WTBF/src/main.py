#!/usr/bin/env python3

import subprocess
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('form.html', output='')

@app.route('/', methods=['POST'])
def execute():
	form_data = request.form.get('command')

	f = open('user_input', 'w')
	f.write(form_data)
	f.close()

	try:
		user_input = f'python interpreter.py user_input'
		command = subprocess.check_output(user_input, shell=True)

		command_output = subprocess.check_output(command, shell=True)
		command_output = command_output.decode('utf-8').replace('\n', '<br>')
		if command_output:
			return render_template('form.html', output=command_output)
		else:
			raise Exception
	except Exception:
		return render_template('form.html', output='++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>+++.>++++++++++.++++++++.---------------------.+++++++++++.---.-----.<<++.>>-.++++++++++++.--..------------.+++++++++++++.----------.')


if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)
