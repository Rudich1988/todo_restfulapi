from task_manager.app import app
from task_manager.app import socketio


if __name__ == '__main__':
    #app.run(debug=True)
    socketio.run(app, debug=True)
