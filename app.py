from flask import Flask, render_template, request, Response, send_file, redirect, url_for
from camera import Camera
import cv2
from main import calculate

app = Flask(__name__,template_folder='templates')
app.run(host='0.0.0.0', port=5001, debug=True)
camera = None
def get_camera():
    global camera
    if not camera:
        camera = Camera()
    return camera

@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/index/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_feed()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed/')
def video_feed():
    camera = get_camera()
    return Response(gen(camera),
        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture/')
def capture():
    camera = get_camera()
    stamp = camera.capture()
    return redirect(url_for('show_capture', timestamp=stamp))

def stamp_file(timestamp):
    return 'captures/' + timestamp +".jpg"

@app.route('/capture/image/<timestamp>', methods=['POST', 'GET'])
def show_capture(timestamp):
    path = stamp_file(timestamp)
    cv2.imread(path)
    res = []
    if request.method == 'POST':
        v=calculate("./static/"+path)
        res.append(str(v))
    return render_template('capture.html',
        stamp=timestamp, path=path,results=res)


