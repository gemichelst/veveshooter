#!/usr/bin/env python3
# coding=utf-8
#

#### IMPORT ####################################################################################################################################################
import os, sys, time, io, json, socket, http.server, socketserver, logging, csv, re, subprocess, tempfile
from bottle import route, run, get, post, request, response, template, static_file


#### VARS #####################################################################################################################################################
DEBUG               = False
HOST_PORT           = 8000
HOST_NAME 	    = socket.gethostname()
HOST_IP             = socket.gethostbyname(HOST_NAME)
WWW_DIR 	    = 'www'
WWW_INDEX           = 'www/index.html'
DATA_DIR            = 'data'
DATA_CSV            = 'data/shoots.csv'
DATA_JSON           = 'data/shoots.json'


#### FUNCTIONS #################################################################################################################################################
def get_Host_name_IP():
    try:
        HOST_NAME = socket.gethostname()
        HOST_IP = socket.gethostbyname(HOST_NAME)
        if DEBUG:
            print("HOSTNAME :  ",HOST_NAME)
            print("IP : ",HOST_IP)
    except:
        print("Unable to get Hostname and IP")

# BASH/SHELL COMMAND AND STDIM
def os_system(command):
    process = Popen(command, stdout=PIPE, shell=True)
    while True:
        line = process.stdout.readline()
        if not line:
            break
        yield line

# ADD SHOOT
def addToShootFile(device,datetime,shoot_minute,shoot_hour,shoot_day,shoot_month):
    shoot_file = './data/shoots.json'

    # DELETE LAST LINE FROM SHOOT_FILE
    fd=open(shoot_file,"r")
    d=fd.read()
    fd.close()
    m=d.split("\n")
    s="\n".join(m[:-1])
    fd=open(shoot_file,"w+")
    for i in range(len(s)):
        fd.write(s[i])
    fd.close()

    # APPEND NEW LINE
    f = open(shoot_file, "a")
    f.write('\n\t\t,{ "device": "' + device + '", "datetime": "' + datetime + '" }\n]')
    f.close()

    # ADD CRONTAB TO USERS CRONFILE
    # MM HH DD MONTH 1-5 echo hello
    cmd_data = shoot_minute + ' ' + shoot_hour + ' ' + shoot_day + ' ' + shoot_month
    cmd = 'veve-add-cron'
    cmd_args = cmd_data
    subprocess.run([cmd, cmd_args])

# PERFORM DROP SHOOT
def dropShootNOW(device,datetime):
    tapX = 500
    tapY = 1450
    cmd = "adb"
    if device=='any':
        cmd_args = 'shell'
        cmd_args += 'input'
        cmd_args += 'tap'
        cmd_args += '500'
        cmd_args += '1450'
    else:
        cmd_args = '-s ' 
        cmd_args += device 
        cmd_args += 'shell'
        cmd_args += 'input'
        cmd_args += 'tap'
        cmd_args += '500'
        cmd_args += '1450'
    subprocess.run([cmd, cmd_args])


#### ROUTES ####################################################################################################################################################

# WWW INDEX
@route('/')
def index():
    return static_file('index.html', root=WWW_DIR)

# WWW FILES
@route('/www/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=WWW_DIR)

# DATA DIR
@route('/data/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=DATA_DIR)

#@route('/www/<filename>')
#def server_static(filename):
#    return static_file(filename, root=WWW_DIR)

# ADD SHOOT
@route('/addShoot', method='GET')
def addShoot():
    device      = request.query.get('device')
    shoot_day   = request.query.get('shoot_day')
    shoot_month = request.query.get('shoot_month')
    shoot_year  = request.query.get('shoot_year')
    shoot_hour  = request.query.get('shoot_hour')
    shoot_minute= request.query.get('shoot_minute')
    datetime    = shoot_year + '-' + shoot_month + '-' + shoot_day + ' ' + shoot_hour + ':' + shoot_minute + ':00';
    addToShootFile(device,datetime,shoot_minute,shoot_hour,shoot_day,shoot_month)
    return template("device: {{device}}\ndatetime: {{datetime}}", device=device, datetime=datetime)

# PERFOM SHOOT
@route('/dropShoot', method='GET')
def dropShoot():
    device      = request.query.get('device')
    datetime    = request.query.get('datetime')
    dropShootNOW(device,datetime)

# GET IP
@route('/getLocalIP', method='GET')
def getLocalIP():
    json_template = template("{{HOST_IP}}", HOST_IP=HOST_IP)
    #return json_template
    json_encoded = json.dumps(json_template, indent=4, sort_keys=True)
    json_decoded = json.loads(json_encoded)
    return { 'HOST_IP': json_decoded, }

# LIST DEVICES FROM ADB
@route('/listDevices', method='GET')
def adbDeviceList():
    with open(os.devnull, 'wb') as devnull:
        out = subprocess.check_output(['adb', 'devices']).splitlines()
    device_list = []
    headers = {}
    for line in out[:2]:
        line = line.decode('utf-8')
        if not line.strip():
            continue
        if 'List' in line:
            continue
        #if 'offline' in line:
        #    continue
        device, _ = re.split(r'\s+', line, maxsplit=1)
        device_list.append(device)

    # RESPONSE AS JSON
    json_encoded = json.dumps(device_list, indent=4, sort_keys=True)
    json_decoded = json.loads(json_encoded)
    return { 'devices': json_decoded, }


#### ACTION ###################################################################################################################################################
if __name__ == "__main__":
	try:
		#print(time.asctime(), "\nHOST_NAME: %s\nHOST_IP: %s\nHOST_PORT: %s" % (HOST_NAME, HOST_IP, HOST_PORT))
		run(host='0.0.0.0', port=HOST_PORT, debug=True)
	except KeyboardInterrupt:
		pass
		print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, HOST_PORT))
