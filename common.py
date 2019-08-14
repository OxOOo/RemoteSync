import glob, os
import hashlib

CONFIG_FILE = '.sync'

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
            data[item.replace(work_dir, '')] = {
                'md5': hashlib.md5(open(item, 'rb').read()).hexdigest(),
                'last_modified': os.path.getmtime(item)
            }
        return data
    else:
        return {}
