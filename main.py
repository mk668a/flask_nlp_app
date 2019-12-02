from flask import *
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, async_mode=None)

value_str = ""  # value_strを定義


@app.route("/")
def init():
    # value_strをhtml側で使えるようにする
    return render_template('index.html', value_str=value_str)

#  action="/input"
@app.route("/input", methods=["GET", "POST"])
def get_form():
    global value_str
    # フォームの値を受け取る
    try:
        value_str = request.form['str']  # name="str"のinputタグの値を取得
    # ページ読み込み時
    except:
        value_str = ""
    # index.html内にて{{ value_str }}で挿入できる
    return render_template('index.html', value_str=value_str)


if __name__ == "__main__":
    # debugはデプロイ時にFalseにする
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)  # 変更
