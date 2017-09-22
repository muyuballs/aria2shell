import json
from base64 import b64encode
from os import path
from urllib import request
import traceback

json_rpc = '2.0'
dash_id = 'pydash'
rpc_address = 'http://127.0.0.1:6800/jsonrpc'
rpc_secret = ''

last_gid = None


def humanize(s):
    if s >= 1024 * 1024 * 1024:
        return "%.2fG" % (s / 1024 / 1024 / 1024)
    if s >= 1024 * 1024:
        return "%.2fM" % (s / 1024 / 1024)
    if s >= 1024:
        return "%.2fK" % (s / 1024)
    return "%.2fB" % s


def print_help():
    print('''Aria2shell By Python v0.1 
method [args]
addr    : set rpc address
secret  : set rpc secret
active  : show active tasks
waiting : show waiting tasks
stopped : show stopped tasks
version : show aria2 version
status  : show task status
adduri  : add url task 
torrent : add torrent task
exit    : exit dash
    ''')
    pass


def get_version():
    try:
        rel = call_rpc('aria2.getVersion')
        if rel:
            obj = json.loads(rel)
            print(obj['result'])
    except Exception:
        print(traceback.print_exc())
    pass


def set_addr():
    global rpc_address
    rpc_address = input("addr:")


def set_secret():
    global rpc_secret
    rpc_secret = input('secret:')


def call_rpc(method, *params):
    try:
        p = ['token:%s' % rpc_secret]
        if params:
            [p.append(x) for x in params]
        body = json.dumps({'jsonrpc': json_rpc, 'id': dash_id, 'method': method, 'params': p}).encode('utf-8')
        req = request.Request(rpc_address, body, method='POST', headers={'Content-Type': 'application/json'})
        resp = request.urlopen(req)
        return resp.read().decode('utf-8')
    except Exception:
        print(traceback.print_exc())


def tell_actives():
    try:
        rel = call_rpc('aria2.tellActive')
        print()
        if rel:
            xrel = json.loads(rel)['result']
            for obj in xrel:
                print('>>> GID:', obj['gid'])
                tl = int(obj['totalLength'])
                cl = int(obj['completedLength'])
                dsp = int(obj['downloadSpeed'])
                for x in obj['files']:
                    xcl = int(x['completedLength'])
                    xl = int(x['length'])
                    print(x['index'], ':', "%s/%s" % (humanize(xcl), humanize(xl)), path.split(x['path'])[-1])

                pres = 0
                if tl != 0:
                    pres = int(cl / tl * 100)
                print('[%s]\t%s/s\t%s/%s (%d%%)' % (
                    obj['status'], humanize(dsp), humanize(cl), humanize(tl), pres))
        print('Total:', len(xrel))
    except Exception:
        print(traceback.print_exc())
    pass


def tell_waiting():
    try:
        offset = int(input("offset:"))
        num = int(input("num:"))
        rel = call_rpc('aria2.tellWaiting', offset, num)
        print()
        if rel:
            xrel = json.loads(rel)['result']
            for obj in xrel:
                print('>>> GID:', obj['gid'])
                tl = int(obj['totalLength'])
                cl = int(obj['completedLength'])
                dsp = int(obj['downloadSpeed'])
                for x in obj['files']:
                    xcl = int(x['completedLength'])
                    xl = int(x['length'])
                    print(x['index'], ':', "%s/%s" % (humanize(xcl), humanize(xl)), path.split(x['path'])[-1])

                pres = 0
                if tl != 0:
                    pres = int(cl / tl * 100)
                print('[%s]\t%s/s\t%s/%s (%d%%)' % (
                    obj['status'], humanize(dsp), humanize(cl), humanize(tl), pres))
        print('Total:', len(xrel))
    except Exception:
        print(traceback.print_exc())
    pass


def tell_stopped():
    try:
        offset = int(input("offset:"))
        num = int(input("num:"))
        rel = call_rpc('aria2.tellStopped', offset, num)
        print()
        if rel:
            xrel = json.loads(rel)['result']
            for obj in xrel:
                print('>>> GID:', obj['gid'])
                tl = int(obj['totalLength'])
                cl = int(obj['completedLength'])
                dsp = int(obj['downloadSpeed'])
                for x in obj['files']:
                    xcl = int(x['completedLength'])
                    xl = int(x['length'])
                    print(x['index'], ':', "%s/%s" % (humanize(xcl), humanize(xl)), path.split(x['path'])[-1])

                pres = 0
                if tl != 0:
                    pres = int(cl / tl * 100)
                print('[%s]\t%s/s\t%s/%s (%d%%)' % (
                    obj['status'], humanize(dsp), humanize(cl), humanize(tl), pres))
        print('Total:', len(xrel))
    except Exception:
        print(traceback.print_exc())
    pass


def tell_status():
    global last_gid
    try:
        gid = input("gid:")
        if not gid:
            gid = last_gid
        else:
            last_gid = gid
        rel = call_rpc('aria2.tellStatus', gid)
        print()
        if rel:
            obj = json.loads(rel)['result']
            print('>>> GID:', obj['gid'])
            tl = int(obj['totalLength'])
            cl = int(obj['completedLength'])
            dsp = int(obj['downloadSpeed'])
            for x in obj['files']:
                xcl = int(x['completedLength'])
                xl = int(x['length'])
                print(x['index'], ':', "%s/%s" % (humanize(xcl), humanize(xl)), path.split(x['path'])[-1])

            pres = 0
            if tl != 0:
                pres = int(cl / tl * 100)
            print('[%s]\t%s/s\t%s/%s (%d%%)' % (
                obj['status'], humanize(dsp), humanize(cl), humanize(tl), pres))
    except Exception:
        print(traceback.print_exc())


def add_url():
    urls = []
    print("please input urls")
    while True:
        url = input("url:")
        if not url:
            break
    if len(urls) < 1:
        print('not url input')
        return
    try:
        rel = call_rpc('aria2.addUri', urls)
        if rel:
            obj = json.loads(rel)
            print("GID:", obj['result'])
    except Exception:
        print(traceback.print_exc())
    pass


def load_from_net(url):
    try:
        return request.urlopen(url).read()
    except Exception:
        print(traceback.print_exc())


def load_from_disk(fp):
    try:
        with open(fp) as f:
            return f.read()
    except Exception:
        print(traceback.print_exc())


def add_torrent():
    print("please input torrent, support load from  http,https,ftp,file or origin torrent encoded by base64")
    torrent = input("torrent:").strip()
    if not torrent:
        print('not torrent input')
        return
    if torrent.startswith('http://') or torrent.startswith('https://') or torrent.startswith('ftp://'):
        torrent = load_from_net(torrent)
    elif torrent.startswith('file://'):
        torrent = load_from_disk(torrent)
    torrent = b64encode(torrent)
    try:
        rel = call_rpc('aria2.addTorrent', torrent)
        if rel:
            obj = json.loads(rel)
            print("GID:", obj['result'])
    except Exception:
        print(traceback.print_exc())
    pass


while True:
    method = input(">>").strip()
    if method == 'help':
        print_help()
    elif method == 'addr':
        set_addr()
    elif method == 'secret':
        set_secret()
    elif method == 'active':
        tell_actives()
    elif method == 'waiting':
        tell_waiting()
    elif method == 'stopped':
        tell_stopped()
    elif method == 'status':
        tell_status()
    elif method == 'version':
        get_version()
    elif method == 'adduri':
        add_url()
    elif method == 'torrent':
        add_torrent()
    elif method == 'exit':
        break
    elif method == '':
        pass
    else:
        print("not supported method")

print('Bye Bye.')
