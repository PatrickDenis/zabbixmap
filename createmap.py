from pyzabbix import ZabbixAPI, ZabbixAPIException
from decouple import config
import csv
import os
import datetime
import calendar

zabbixuser = config('USERNAME')
zabbixpassword= config('PASSWORD')

zapi = ZabbixAPI("http://192.168.12.12/zabbix", user=zabbixuser, password=zabbixpassword)
#print('Enter map name:')
mapname = 'mymap'
map = zapi.map.get({"filter": {"name": mapname}})
mapid = map[0]['sysmapid']
#print(map)
hosts = zapi.host.get(selectGroups='extend')
host_element = []
for host in hosts:
    if(host['host'] == 'proxy'):
    	pfsenseid = host['hostid']
    elif(host['host'] == 'zabbix server'):
    	zabbixid = host['hostid']
#    print(host)
icons = {
    "zabbixserver": 187,
    "cloud": 5,
    "server": 151,
    "router": 126,
    "switch": 156,
}

map_elements = []
xcor = 100
ycor = 520
xxcor = 100
yycor = 100
links = []
for host in hosts:
    map_element = {}
    map_element['selementid'] = host['hostid']
    map_element['elements'] = []
    element = {}
    element['hostid'] = host['hostid']
    map_element['elements'].append(element)
    map_element['elementtype'] = "0"
    if(host['host'] == 'zabbixserver'):
    	map_element['iconid_off'] = icons['zabbixserver']
    else:
	map_element['iconid_off'] = icons['server']
    if(host['host'] == 'zabbixserver'):
    	map_element['x'] = 850
    	map_element['y'] = 300
    elif(host['host'] == 'proxy'):
    	map_element['x'] = 850
        map_element['y'] = 420
    elif(host['proxy_hostid'] == '0'):
	map_element['x'] = xxcor
        map_element['y'] = yycor
	xxcor = xxcor + 200
        if(xxcor >= 1820):
                yycor = yycor + 200
                xxcor = 100
    else:
   	map_element['x'] = xcor
    	map_element['y'] = ycor
        xcor = xcor + 200
        if(xcor >= 1820):
        	ycor = ycor + 200
 		xcor = 100
    
    map_elements.append(map_element)

    link = {}
    if(host['proxy_hostid'] == '0'):
    	link['selementid1'] = zabbixid
    	link['selementid2'] = host['hostid']
    	link['color'] = "00CC00"
    else:
   	link['selementid1'] = proxyid
        link['selementid2'] = host['hostid']
        link['color'] = "00CC00"
    links.append(link)

new_map = zapi.map.update(name=mapname,
			  sysmapid=mapid,
                          width="1920",
                          height="2000",
                          selements=map_elements,
                          links=links
                          )


