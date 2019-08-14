# encoding: utf-8

import os, sys, time, math
import common
import requests, json

WORK_DIR = os.path.abspath(os.path.curdir)
if len(sys.argv) > 1:
    WORK_DIR = os.path.abspath(sys.argv[1])
HOST = 'http://localhost:2333'

cnt = 0
def process():
    global cnt
    cnt = cnt + 1
    remote_time = float(requests.get(HOST + '/time').text)
    delta_time = math.fabs(remote_time-time.time()) * 3
    if cnt % 10 == 1: print('delta:', round(delta_time))

    local_data = common.walk(WORK_DIR)
    remote_data = json.loads(requests.get(HOST + '/walk').text)

    for item in local_data.keys():
        upload = False
        if item not in remote_data.keys():
            upload = True
        elif remote_data[item]['md5'] != local_data[item]['md5'] and local_data[item]['last_modified'] > remote_data[item]['last_modified'] + delta_time:
            upload = True
        # upload
        if upload:
            files = {'file': open(os.path.join(WORK_DIR, item), 'rb')}
            requests.post(HOST + '/upload/' + item, files=files)
            print('[%s U] %s' % (time.strftime('%H:%M'), item))
    for item in remote_data.keys():
        download = False
        if item not in local_data.keys():
            download = True
        elif remote_data[item]['md5'] != local_data[item]['md5'] and local_data[item]['last_modified'] + delta_time < remote_data[item]['last_modified']:
            download = True
        # download
        if download:
            r = requests.get(HOST + '/download/' + item)
            os.makedirs(os.path.dirname(os.path.join(WORK_DIR, item)), exist_ok=True)
            with open(os.path.join(WORK_DIR, item), 'wb') as fd:
                fd.write(r.content)
            print('[%s D] %s' % (time.strftime('%H:%M'), item))

if __name__ == '__main__':
    while True:
        process()
        time.sleep(1)
