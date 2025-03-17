from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        message = request.form.get('message', '').strip()

        if not username or not message:
            return "Error: Both fields are required!", 400

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_message = {timestamp: {"username": username, "message": message}}

        # Читаємо або створюємо data.json
        data_file = 'storage/data.json'
        if not os.path.exists('storage'):
            os.makedirs('storage')

        try:
            with open(data_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        # Додаємо нове повідомлення
        data.update(new_message)

        # Записуємо у файл
        with open(data_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        return redirect(url_for('index'))

    return render_template('message.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html"), 404

@app.route('/read')
def read_messages():
    data_file = 'storage/data.json'

    try:
        with open(data_file, 'r', encoding='utf-8') as file:
            messages = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messages = {}

    return render_template('read.html', messages=messages)


if __name__ == '__main__':
    print("Starting Flask server...")  # Додаємо повідомлення перед запуском
    app.run(debug=True, port=3000)
