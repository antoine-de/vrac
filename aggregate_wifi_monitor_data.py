from clingon import clingon
import subprocess
import os
import select

#from: http://stackoverflow.com/questions/7729336/how-can-i-print-and-display-subprocess-stdout-and-stderr-output-without-distorti/7730201#7730201
import fcntl
import errno
import jsonpickle
import datetime
import re

SNIFFER_ID = "antoine"

def parse_log(buff):
    logs = []
    line, sep, buff = buff.partition('\n')
    while sep and buff:
        logs.append(line)
        line, sep, buff = buff.partition('\n')
    if not sep:
        buff = line
    return logs, buff


def make_async(fd):
    fcntl.fcntl(fd, fcntl.F_SETFL, fcntl.fcntl(fd, fcntl.F_GETFL) | os.O_NONBLOCK)


def read_async(fd):
    try:
        return fd.read()
    except IOError, e:
        if e.errno != errno.EAGAIN:
            raise e
        else:
            return ''

def stream_data(wlan):
    """ Launch an exec with args, log the outputs """
    args = "tcpdump -i {} -e -s 256 type mgt  subtype probe-req -v".format(wlan).split(' ')
    proc = subprocess.Popen(args,
                            stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            close_fds=True)
    try:
        make_async(proc.stderr)
        make_async(proc.stdout)
        while True:
            select.select([proc.stdout, proc.stderr], [], [])

            for pipe in proc.stdout, proc.stderr:
                log_pipe = read_async(pipe)
                logs, line = parse_log(log_pipe)
                for l in logs:
                    yield l

            if proc.poll() is not None:
                break
    finally:
        proc.stdout.close()
        proc.stderr.close()


class Prob(object):
    def __init__(self, tcpdump_line):
        current_date = datetime.datetime.now()

        fields = tcpdump_line.split(' ')

        raw_date = fields[0]

        raw_noise = fields[6]
        try:
            n = int(raw_noise.replace('-', '').replace('dB', ''))
        except:
            n = -1

        mac_regexp = re.compile('SA(:..:..:..:..:..:..)')
        m = mac_regexp.search(tcpdump_line)
        mac = ''
        if m:
            mac = m.group(1)
        self.mac = mac
        self.sniffer_id = SNIFFER_ID
        time = raw_date.replace(":", "")
        self.datetime = "{d}T{t}".format(d=current_date.strftime("%Y%m%d"), t=time)
        self.noise = n

        remaining_regexp = re.compile('Probe Request \((.*)\)')
        ssid = ''
        s = remaining_regexp.search(tcpdump_line)
        if s:
            ssid = s.group(1)
        self.requested_ssid = ssid


def send(bucket, api):

    print "exporting: {}".format(jsonpickle.encode(bucket))
    import requests
    r = requests.post('{api}/prob'.format(api=api), data=jsonpickle.encode(bucket))

    print "post ? {}, {}".format(r.status_code, r.text)


@clingon.clize()
def send_monitor_data(wlan, api='http://10.50.82.60/www/api-dev.php/api', bucket_limit=100):

    bucket = []
    for d in stream_data(wlan):
        if len(d.split(' ')) < 7:
            continue
        bucket.append(Prob(d))

        if len(bucket) > bucket_limit:
            print 'flushing bucket'
            # we flush
            send(bucket, api)
            print "data send"
            bucket = []






