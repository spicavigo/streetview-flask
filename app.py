from flask import Flask, url_for, jsonify, redirect
from flask import render_template
from datetime import date
import json
from functools import wraps
from flask import redirect, request, current_app
import os
import shutil
import uuid
import urllib2

app = Flask(__name__)
KEY = 'AIzaSyAUuoxYS81W9KvpXJCZX2NjURVMoMCswII'

@app.route('/')
def index():
    return render_template('index.html', key=KEY)

@app.route('/get_video')
def getVideo():
    url = []
    for e in request.args.getlist('data[]'):
        lat, lng, bearing = e.split(',')
        url.append("http://maps.googleapis.com/maps/api/streetview?size=600x300&location="+ lat +"," + lng +"&heading="+bearing+"&pitch=-1.62&sensor=false&key="+KEY)
    u = 'static/' + str(uuid.uuid4())
    try:
        shutil.rmtree(u)
    except OSError:pass
    os.mkdir(u)
    for index, e in enumerate(url):
        uo=urllib2.urlopen(e)
        f=open("%s/%05d.jpg" % (u, index), 'w')
        f.write(uo.read())
        f.close()
    os.system("mencoder mf://%s/*.jpg -mf type=jpg:fps=4 -ovc lavc -lavcopts vcodec=wmv2 -oac copy -o %s/output.avi" % (u,u))
    return '%s/output.avi' % u
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
