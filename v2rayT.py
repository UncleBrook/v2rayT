#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import os
import requests
import base64
import json
import subprocess
import re


v2rayT_path = os.path.expandvars('$HOME') + '/.v2rayT/'
v2rayT_sub_path = v2rayT_path + '/.v2rayT.sub'
v2rayT_config_path = v2rayT_path + '/.v2rayT.conf'

if not os.path.exists(v2rayT_path):
    os.mkdir(v2rayT_path, mode=0o777)

if not os.path.exists(v2rayT_sub_path):
    open(v2rayT_sub_path, 'w+')

if not os.path.exists(v2rayT_config_path):
    open(v2rayT_config_path, 'w+')


def addSubUrl():
    sub_url = input('Please enter the subscription url: ')
    sub_file = open(v2rayT_sub_path, 'w+')
    sub_file.write(sub_url)
    sub_file.close()
    return sub_url


def addConfigs(content):
    configs = str(base64.urlsafe_b64decode(content), encoding="utf-8")
    config_file = open(v2rayT_config_path, 'w+')
    config_file.write(configs)
    config_file.close()
    return configs


def readConfigs():
    config_file = open(v2rayT_config_path, 'r')
    configs = config_file.read().strip()
    config_file.close()
    return configs


v2rayT_sub_file = open(v2rayT_sub_path, 'r')
v2rayT_sub_url = v2rayT_sub_file.read().strip()
v2rayT_sub_file.close()


def loadSubContent():
    try:
        content = requests.get(v2rayT_sub_url).content
        missingPadding = 4 - len(content) % 4
        if missingPadding:
            content += b'=' * missingPadding
        return content
    except:
        print('Error address: ' + v2rayT_sub_url + ', please check')
        os.remove(v2rayT_sub_path)
        os.remove(v2rayT_config_path)
        exit()


v2rayT_configs = ''
if not v2rayT_sub_url:
    v2rayT_sub_url = addSubUrl()
    v2rayT_configs = addConfigs(loadSubContent())
else:
    while True:
        branch = int(input(
            'Please choose what you want to continue: \n [1] Resubscribe\n [2] Refresh Config\n [3] Continue \nPlease enter your selection number: '))
        if branch == 1:
            v2rayT_sub_url = addSubUrl()
            v2rayT_configs = addConfigs(loadSubContent())
            break
        elif branch == 2:
            v2rayT_configs = addConfigs(loadSubContent())
            break
        elif branch == 3:
            v2rayT_configs = readConfigs()
            break


print('\n')
server_list = str.encode(v2rayT_configs).splitlines()
for i in range(len(server_list)):
    server_node = json.loads(base64.b64decode(
        bytes.decode(server_list[i]).replace('vmess://', '')))
    print(' [' + str(i) + '] ' + server_node['ps'])
    server_list[i] = server_node


while True:
    checked_node_id = int(input("\nPlease enter the node number to use："))
    subprocess.call(
        '\nping ' + server_list[checked_node_id]['add'] + ' -c 3 -w 10', shell=True)
    yes_or_no = input('\nAre you sure you want to use this node?[y/N] ')
    if re.search('[yesYES]', yes_or_no):
        break
    elif re.search('[noNO]', yes_or_no):
        exit()


address = server_list[checked_node_id]['add']
port = int(server_list[checked_node_id]['port'])
alter_id = server_list[checked_node_id]['aid']
users_id = server_list[checked_node_id]['id']

v2ray_config = {
    "dns": {
        "servers": [
            "1.1.1.1"
        ]
    },
    "inbounds": [
        {
            "listen": "127.0.0.1",
            "port": 10809,
            "protocol": "socks",
            "settings": {
                "auth": "noauth",
                "udp": True,
                "userLevel": 8
            },
            "sniffing": {
                "destOverride": [
                    "http",
                    "tls"
                ],
                "enabled": True
            },
            "tag": "socks"
        },
        {
            "listen": "127.0.0.1",
            "port": 10808,
            "protocol": "http",
            "settings": {
                "userLevel": 8
            },
            "tag": "http"
        }
    ],
    "log": {
        "loglevel": "warning"
    },
    "outbounds": [
        {
            "mux": {
                "enabled": False
            },
            "protocol": "vmess",
            "settings": {
                "vnext": [
                    {
                        "address": address,
                        "port": port,
                        "users": [
                            {
                                "alterId": alter_id,
                                "id": users_id,
                                "level": 8,
                                "security": "auto"
                            }
                        ]
                    }
                ]
            },
            "streamSettings": {
                "network": "ws",
                "security": "",
                "wssettings": {
                    "connectionReuse": True,
                    "headers": {
                        "Host": ""
                    },
                    "path": "video"
                }
            },
            "tag": "proxy"
        },
        {
            "protocol": "freedom",
            "settings": {},
            "tag": "direct"
        },
        {
            "protocol": "blackhole",
            "settings": {
                "response": {
                    "type": "http"
                }
            },
            "tag": "block"
        }
    ],
    "policy": {
        "levels": {
            "8": {
                "connIdle": 300,
                "downlinkOnly": 1,
                "handshake": 4,
                "uplinkOnly": 1
            }
        },
        "system": {
            "statsInboundUplink": True,
            "statsInboundDownlink": True
        }
    },
    "routing": {
        "domainStrategy": "IPIfNonMatch",
        "rules": [
            {
                "domain": [
                    "domain:googleapis.cn"
                ],
                "outboundTag": "proxy",
                "type": "field"
            },
            {
                "ip": [
                    "geoip:private"
                ],
                "outboundTag": "direct",
                "type": "field"
            },
            {
                "ip": [
                    "geoip:cn"
                ],
                "outboundTag": "direct",
                "type": "field"
            },
            {
                "domain": [
                    "geosite:cn"
                ],
                "outboundTag": "direct",
                "type": "field"
            }
        ]
    },
    "stats": {}
}

json.dump(v2ray_config, open('/etc/v2ray/config.json', 'w'), indent=2)

print("\nRestart v2ray...")
subprocess.call('sudo systemctl restart v2ray.service', shell=True)
print('Well done, it\'s completed')

exit()
