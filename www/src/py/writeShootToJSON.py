#!/usr/bin/env python3
# WRITE SHOOZ DATA TO SHOOT.JSON
# USAGE: writeShootToJSON.py vars
#
print('Content-type: application/python\n')

#### IMPORT ###############################################################################################
import sys


#### VARS ################################################################################################
shootID 	= sys.argv[1]
shootDAY	= sys.argv[2]
shootMONTH	= sys.argv[3]
shootYEAR	= sys.argv[4]
shootHOUR	= sys.argv[5]
shootMINUTE	= sys.argv[6]
filePath = "../../../data/shoots.json"
#print filePath

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)


#### ACTION ##############################################################################################
f = open(filePath, "w")
f.write('{ "title": "' + deviceTitle + '", "deviceID": ' + deviceID + ', "usbID": "' + deviceUsbID + '", "desc": "' + deviceDesc + '", "icon": "' + deviceIcon + '" }')
f.close()
