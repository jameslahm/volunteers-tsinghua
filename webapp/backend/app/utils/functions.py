# -*- coding: utf-8 -*-
'''通用零散的函数封装'''
import os
from datetime import datetime
import uuid
import re
import hashlib
from urllib.parse import (
        urlencode,
        parse_qs,
        urlsplit,
        urlunsplit
    )


def md5(origin_str):
    '''计算md5'''
    m5 = hashlib.md5()
    try:
        m5.update(origin_str)
    except (TypeError, UnicodeEncodeError):
        m5.update(origin_str.encode('utf-8', 'ignore'))
    return m5.hexdigest()
