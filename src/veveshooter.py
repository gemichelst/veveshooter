#!/usr/bin/env python3
# coding=utf-8
#

#### IMPORT ####################################################################################################################################################
import os, time, io, json, socket, http.server, socketserver, logging, csv, re, subprocess, tempfile
from bottle import route, run, get, post, request, response, template, static_file


#### VARS #####################################################################################################################################################
HOST_PORT           = 8000
HOST_NAME 	        = socket.gethostname()
HOST_IP             = '0.0.0.0'
WWW_DIR 	        = 'www'
WWW_INDEX           = 'www/index.html'
DATA_DIR            = 'data'
DATA_CSV            = 'data/shoots.csv'
DATA_JSON           = 'data/shoots.json'


#### FUNCTIONS #################################################################################################################################################
def get_Host_name_IP():
    try:
        HOST_NAME = socket.gethostname()
        HOST_IP = socket.gethostbyname(HOST_NAME)
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

# SAVE DEVICE CONF
def saveDeviceFile(device_file,device_id,device_title,device_usbid,device_desc,device_icon):
    f = open(device_file, "w")
    f.write('{ "title": "' + device_title + '", "deviceID": ' + device_id + ', "usbID": "' + device_usbid + '", "desc": "' + device_desc + '", "icon": "' + device_icon + '" }')
    f.close()


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

# SAVE DEVICES
# @route('/saveDevice', method='GET')
# def saveDevice():
#     device_id       = request.query.get('id')
#     device_title    = request.query.get('devicename')
#     device_usbid    = request.query.get('usbid')
#     device_desc     = request.query.get('desc')
#     device_icon     = request.query.get('icon')
#     device_file     = CONF_DEVICES_DIR + '/device_' + device_id + '.json'
#     saveDeviceFile(device_file,device_id,device_title,device_usbid,device_desc,device_icon)
#     return template("device_id: {{device_id}}\ndevice_title: {{device_title}}\ndevice_usbid: {{device_usbid}}\ndevice_desc: {{device_desc}}\ndevice_icon: {{device_icon}}\n device_file: {{device_file}}", device_id=device_id, device_title=device_title, device_usbid=device_usbid, device_desc=device_desc, device_icon=device_icon, device_file=device_file)

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
	print(time.asctime(), "\nHOST: %s:%s\nIP: %s\nWWW: %s" % (HOST_NAME, HOST_PORT, HOST_IP, WWW_DIR))
	try:
		run(host='0.0.0.0', port=HOST_PORT, debug=True)
	except KeyboardInterrupt:
		pass
		print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, HOST_PORT))
