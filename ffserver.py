from flask import Flask, request, jsonify
from subprocess import Popen, PIPE
import uuid
import os
import json

app = Flask("ffserver", static_url_path='')
processing = False

@app.route("/")
def root():
    return app.send_static_file("index.html")

@app.route("/ffmpeg", methods=['POST'])
def ffmpeg():
    global processing
    if processing == True:
        return jsonify({ "result": "processing..." })
    processing = True

    vidID = str(uuid.uuid4())
    outDir = "static/" + vidID
    os.makedirs(outDir)
    cmd = request.json["cmd"].replace("ffmpeg ", "").replace("\"", "")
    cmdArgs = ["ffmpeg", "-loglevel", "error"]
    for c in cmd.split(" "):
        cmdArgs.append(c)
    proc = Popen(cmdArgs, cwd=outDir, stdout=PIPE, stderr=PIPE)
    stdout, stderr = proc.communicate()

    result = proc.wait()
    processing = False
    if result == 1:
        os.rmdir(outDir)
        return jsonify({"error": stderr})
    return jsonify({ "result": vidID + "/" + cmdArgs[-1] })

if __name__ == "__main__":
    app.run(host='0.0.0.0')
