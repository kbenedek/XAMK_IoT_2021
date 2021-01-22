

#Based on: https://nostarch.com/RaspberryPiProject



import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server

PAGE="""\
<html>
<head>
<title>Raspberry Surveillance Camera</title>
<style>
    .wrapper { 
  height: 100%;
  width: 100%;
  left:0;
  right: 0;
  top: 0;
  bottom: 0;
  position: absolute;
background: linear-gradient(124deg, #ff2400, #e81d1d, #e8b71d, #e3e81d, #1de840, #1ddde8, #2b1de8, #dd00f3, #dd00f3);
background-size: 1800% 1800%;

-webkit-animation: rainbow 18s ease infinite;
-z-animation: rainbow 18s ease infinite;
-o-animation: rainbow 18s ease infinite;
  animation: rainbow 18s ease infinite;}

@-webkit-keyframes rainbow {
    0%{background-position:0% 82%}
    50%{background-position:100% 19%}
    100%{background-position:0% 82%}
}
@-moz-keyframes rainbow {
    0%{background-position:0% 82%}
    50%{background-position:100% 19%}
    100%{background-position:0% 82%}
}
@-o-keyframes rainbow {
    0%{background-position:0% 82%}
    50%{background-position:100% 19%}
    100%{background-position:0% 82%}
}
@keyframes rainbow { 
    0%{background-position:0% 82%}
    50%{background-position:100% 19%}
    100%{background-position:0% 82%}
}
@keyframes example {
  0%   {width: 100%; height:25%}
  25%  {width: 50%; height: 50%}
  50%  {width: 25%; height: 100%}
  75%  {width: 50%; height: 50%}
  100% {width: 100%; height:25%}
}

.boing {
  animation-name: example;
  animation-duration: 4s;
  animation-iteration-count: infinite;
    margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
}
</style>
</head>
<body>
<div class="wrapper">
<center><h1 style="background-image: linear-gradient(to left, violet, indigo, blue, green, yellow, orange, red);   -webkit-background-clip: text;
  color: transparent; font-family: 'font-family: "Comic Sans MS", "Comic Sans", cursive;">Raspberry Pi - Surveillance Camera</h1></center>
<center ><img class="boing" src="stream.mjpg" width="640" height="480"></center>
</div>
</body>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            #new frame, copy the existing buffer's content and notify all
            #clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
