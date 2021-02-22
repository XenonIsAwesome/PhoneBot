from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request, session, url_for, redirect, abort
from db_connection import connect


app = Flask(__name__)
app.secret_key = 'add-yours'

# socket io
sio = SocketIO(app, async_mode='eventlet', manage_session=False, cors_allowed_origins='*')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/project')
def project():
    return render_template('project.html')


@app.route('/creator')
def creator():
    return render_template('creator.html')


@sio.on('request_update')
def on_request_update(data):
    db = connect()
    stats = db.find_one({'statistics': True})

    emit("send_update", stats['guild_amount'])


@sio.on('error')
def on_error(data):
    raise(data['content'])


if __name__ == '__main__':
    sio.run(app, debug=True, use_reloader=True, port=5000)
