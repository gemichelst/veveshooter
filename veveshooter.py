#!/usr/bin/env python3
# coding=utf-8
#

import os, time, io, json, socket, http.server, socketserver, logging, csv, re, subprocess, tempfile
from bottle import route, run, get, post, request, response, template, static_file


#####################################################################
# ADB DEVICES OUTPUT ################################################
#####################################################################
class FindDeviceError(RuntimeError):
    pass
class DeviceNotFoundError(FindDeviceError):
    def __init__(self, serial):
        self.serial = serial
        super(DeviceNotFoundError, self).__init__(
            'No device with serial {}'.format(serial))
class NoUniqueDeviceError(FindDeviceError):
    def __init__(self):
        super(NoUniqueDeviceError, self).__init__('No unique device')
def adbDeviceList():
    with open(os.devnull, 'wb') as devnull:
        out = subprocess.check_output(['adb', 'devices']).splitlines()
    devices = []
    for line in out[:2]:
        line = line.decode('utf-8')
        line = line.replace("\"", "'")
        if not line.strip():
            continue
        if 'List' in line:
            continue
        #if 'offline' in line:
        #    continue
        serial, _ = re.split(r'\s+', line, maxsplit=1)
        devices.append(serial)
    return(devices)
#####################################################################
# HTTP.SERVER #######################################################
#####################################################################
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/www/index.html'
        if self.path == '/devices':
            json_encoded = json.dumps('{ "devices":' + print(adbDeviceList()) + '}')
            json_decoded = json.loads(json_encoded)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            #print('{ "devices": ', adbDeviceList(), '}')
            #data_stream = adbDeviceList()
            #data_replace = data_stream.replace("'", "\"")
            # data_dump = json.dumps(data_stream)
            # data = json.loads(data_dump)
            # data_final = data.replace("'", "\"")
            # print(data_final)
            # RESPONSE AS JSON
            
            #print('{ "devices":', json_decoded, '}')
            #return('{ "devices":', json_decoded, '}')
            #devices = '{ "devices":', json_decoded, '}'
            self.wfile.write(json_encoded)
            #return adbDeviceList();

        return http.server.SimpleHTTPRequestHandler.do_GET(self)
        

def adbServerInit():
    with open(os.devnull, 'wb') as devnull:
        print('ADB:\t[KILL-SERVER]')
        subprocess.run(["adb", "kill-server"])
        print('ADB:\t[START-SERVER]')
        subprocess.check_call(['adb', 'start-server'], stdout=devnull, stderr=devnull)
        print('ABD:\t[STARTED]')

def wwwServerInit():
    handler_object = MyHttpRequestHandler
    PORT = 8000
    my_server = socketserver.TCPServer(("", PORT), handler_object)
    print('WWW:\t[STARTED]')
    my_server.serve_forever()
    

# ADB INIT
adbServer = adbServerInit();

# WWW INIT
wwwServer = wwwServerInit();