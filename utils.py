import json
import logging
import platform
import re
import socket
import uuid

import psutil


def getSystemInfoDict():
    try:
        info = dict()
        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['hostname'] = socket.gethostname()
        info['ip-address'] = socket.gethostbyname(socket.gethostname())
        info['mac-address'] = ':'.join(re.findall('..',
                                                  '%012x' % uuid.getnode()))
        info['processor'] = platform.processor()
        info['ram'] = str(
            round(psutil.virtual_memory().total / (1024.0 ** 3)))+" GB"
        return info
    except Exception as e:
        logging.exception(e)


def getSystemInfoString():
    return json.dumps(getSystemInfoDict())


def getSystemInfoJson():
    return json.loads(getSystemInfoString())
