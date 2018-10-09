#!/usr/bin/env python
# -*- coding:utf-8 -*-

import argparse
import shutil
import sys
import os
from io import StringIO

USERAGENT = 'tis/download.py_1.0--' + sys.version.replace('\n', '').replace('\r', '')


def geturl(url, token=None, out=None):
    headers = {'user-agent': USERAGENT}
    if not token is None:
        headers['Authorization'] = 'Bearer ' + token
    try:
        import ssl
        CTX = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        if sys.version_info.major == 2:
            import urllib2
            try:
                fh = urllib2.urlopen(urllib2.Request(url, headers=headers), context=CTX)
                if out is None:
                    return fh.read()
                else:
                    shutil.copyfileobj(fh, out)
            except urllib2.HTTPError as e:
                print('HTTP GET error code: %d' % e.code(), file=sys.stderr)
                sys.stdout.flush()
                print('HTTP GET error message: %s' % e.message, file=sys.stderr)
                sys.stdout.flush()
            except urllib2.URLError as e:
                print('Failed to make request: %s' % e.reason, file=sys.stderr)
                sys.stdout.flush()
            return None

        else:
            from urllib.request import urlopen, Request, URLError, HTTPError
            try:
                fh = urlopen(Request(url, headers=headers), context=CTX)
                if out is None:
                    return fh.read().decode('utf-8')
                else:
                    # print('welldone')
                    shutil.copyfileobj(fh, out)
            except HTTPError as e:
                print('HTTP GET error code: %d' % e.code(), file=sys.stderr)
                sys.stdout.flush()
                print('HTTP GET error message: %s' % e.message, file=sys.stderr)
                sys.stdout.flush()
            except URLError as e:
                print('Failed to make request: %s' % e.reason, file=sys.stderr)
                sys.stdout.flush()
            return None

    except AttributeError:
        # OS X Python 2 and 3 don't support tlsv1.1+ therefore... curl
        import subprocess
        try:
            args = ['curl', '--fail', '-sS', '-L', '--get', url]
            for (k, v) in headers.items():
                args.extend(['-H', ': '.join([k, v])])
            if out is None:
                # python3's subprocess.check_output returns stdout as a byte string
                result = subprocess.check_output(args)
                return result.decode('utf-8') if isinstance(result, bytes) else result
            else:
                subprocess.call(args, stdout=out)
        except subprocess.CalledProcessError as e:
            print('curl GET error message: %' + (e.message if hasattr(e, 'message') else e.output), file=sys.stderr)
            sys.stdout.flush()
        return None


def sync(src, dest, tok):
    """synchronize src url with dest directory """
    try:
        import csv
        files = [f for f in csv.DictReader(StringIO(geturl('%s.csv' % src, tok)), skipinitialspace=True)]
    except ImportError:
        import json
        files = json.loads(geturl(src + '.json', tok))

    total_num = len(files)
    print('The number of files is:', total_num)
    sys.stdout.flush()

    # use os.path since python 2/3 both support it while pathlib is 3.4+
    order = 0
    for f in files:
        # currently we use filesize of 0 to indicate directory
        order += 1
        filesize = int(f['size'])
        path = os.path.join(dest, f['name'])
        url = src + '/' + f['name']
        if filesize == 0:
            try:
                print('creating dir:', path)
                sys.stdout.flush()
                os.mkdir(path)
                sync(src + '/' + f['name'], path, tok)
            except IOError as e:
                print("mkdir `%s': %s" % (e.filename, e.strerror), file=sys.stderr)
                sys.stdout.flush()
                sys.exit(-1)
        else:
            try:
                if not os.path.exists(path):
                    print('[', order, '/', total_num, ']  downloading: ', path)
                    sys.stdout.flush()
                    with open(path, 'w+b') as fh:
                        geturl(url, tok, fh)
                else:
                    print('[', order, '/', total_num, ']  skipping: ', path)
                    sys.stdout.flush()
            except IOError as e:
                print("open `%s': %s" % (e.filename, e.strerror), file=sys.stderr)
                sys.stdout.flush()
                sys.exit(-1)
    return 0


def _main(argv):
    parser = argparse.ArgumentParser(prog=argv[0], description='hello')
    parser.add_argument('-s', '--source', dest='source', metavar='URL', help='Recursively download files at URL',
                        required=True)
    parser.add_argument('-d', '--destination', dest='destination', metavar='DIR',
                        help='Store directory structure in DIR', required=True)
    parser.add_argument('-t', '--token', dest='token', metavar='TOK', help='Use app token TOK to authenticate',
                        required=True)
    args = parser.parse_args(argv[1:])
    if not os.path.exists(args.destination):
        os.makedirs(args.destination)
    return sync(args.source, args.destination, args.token)


if __name__ == '__main__':
    try:
        sys.exit(_main(sys.argv))
    except KeyboardInterrupt:
        sys.exit(-1)
