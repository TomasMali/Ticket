

import subprocess

def getSid():
    p = subprocess.Popen(['node', 'sid.js'], stdout=subprocess.PIPE)
    out = str(p.stdout.read())
    out_format = (out[2:])[:-3]
    print(out_format)
    return out_format

getSid()
