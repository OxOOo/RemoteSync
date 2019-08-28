import glob, os
import hashlib

CONFIG_FILE = '.sync'

global ginfo
ginfo = {}
def getinfo(filepath):
    global ginfo
    filepath = os.path.abspath(filepath)
    if filepath not in ginfo or ginfo[filepath]['last_modified'] != os.path.getmtime(filepath):
        ginfo[filepath] = {
            'md5': hashlib.md5(open(filepath, 'rb').read()).hexdigest(),
            'last_modified': os.path.getmtime(filepath)
        }
    return ginfo[filepath]

def walk(work_dir):
    work_dir = os.path.join(work_dir, './')
    if os.path.exists(os.path.join(work_dir, CONFIG_FILE)):
        files = []
        notfiles = []
        for line in open(os.path.join(work_dir, CONFIG_FILE), 'r'):
            line = line.strip()
            if len(line) == 0: continue
            if line.startswith('~'):
                notfiles.extend(glob.glob(os.path.join(work_dir, line[1:])))
            else:
                files.extend(glob.glob(os.path.join(work_dir, line)))
        
        data = {}
        for item in files:
            if item in notfiles: continue
            if not os.path.isfile(item): continue
            assert work_dir in item
            data[item.replace(work_dir, '')] = getinfo(item)
        return data
    else:
        return {}
