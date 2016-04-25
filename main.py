#!/usr/bin/python

from flask import Flask, render_template, send_from_directory, request, Response
import datetime
from functools import wraps
import logging
from logging import FileHandler
import os
from werkzeug.contrib.profiler import ProfilerMiddleware
import json
import iso8601

import datetime
import pytz

app = Flask(__name__)

if False and not app.debug:
    file_handler = FileHandler('/var/log/peteFlask')
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)
    

@app.route('/')
def root():
    return "<a href='/13:00/Brussels'>demo</a>"

@app.route('/test/<time>/<zonename1>/<zonename2>')
def dstTime2(time,zonename1,zonename2):
    return dstTime(time,zonename1+"/"+zonename2)

@app.route('/test/<time>/<zonename>')
def dstTime(time,zonename):
    #dstDiv=render_template('dstdiv.html', newTime=newTime,theTime=theTime,date=date,url="/%s/%s"%(time,zone))
    newTzinfo = calculateTimezone(zonename)
    theTime = iso8601.parse_date(time)
    newTime = theTime.astimezone(newTzinfo)
    if None:
        return '''<div id="dstDiv">dit is een test %s
                <br/>%s
                </div>'''%(str(time) +"/"+ zonename, newTime)
    return render_template('dstdiv.html', newTime=newTime,date=None)

@app.route('/favicon.ico')
def favicon():
    return ""

@app.route('/<time>')
def timeZone0(time):
    return timeZone(time,'UTC')

@app.route('/<time>/<zone>')
def timeZone(time,zone):
    #source time zone
    tzinfo = calculateTimezone(zone)

    #target timezone
    if request.args.get('to'):
        toName = request.args.get('to')
    else:
        toName = "UTC"
    
    #parse time
    if ('T' in time) or (" " in time) or ("+" in time) or ("_" in time):
        t = time.replace(" ","T").replace("+","T").replace("_","T")
        theTime = tzinfo.localize(datetime.datetime.strptime(t,"%Y-%m-%dT%H:%M"))
        date = theTime.date()
    else:
        t = str(datetime.date.today())+"T"+time
        theTime = tzinfo.localize(datetime.datetime.strptime(t,"%Y-%m-%dT%H:%M"))
        date= None
    
    
    dstDiv=dstTime(str(theTime),toName)
    
    return render_template('time.html',
                           theTime=theTime,
                           date=date,url="/%s/%s"%(time,zone)).replace('<div id="dstDiv"></div>', dstDiv)

def calculateTimezone(name):
    for prefix in ["Europe/","US/","Asia/","Africa/","Australia/",""]:
        try:
            zone = prefix + name.replace('-','/')
            return pytz.timezone(zone)
        except pytz.exceptions.UnknownTimeZoneError as e:
            None
    raise e
if __name__ == '__main__':
    app.debug = True
    f = open('/tmp/profiler.log', 'a')
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, f)
    app.run()
