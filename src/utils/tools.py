# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import cgi
import re
import string
import random

re_string = re.compile(r'(?P<htmlchars>[<&>])|(?P<space>^[ \t]+)|(?P<lineend>\r\n|\r|\n)|(?P<protocal>(^|\s)((http|ftp|https)://.*?))(\s|$)', re.S|re.M|re.I)


def plaintext2html(text, tabstop=4):
    """
    Convert plaint text with spaces or contains URLs to HTML string

    :param text: original text
    :param tabstop: tab space count, default to 4
    :return: converted HTML string
    """
    def do_sub(m):
        c = m.groupdict()
        if c['htmlchars']:
            return cgi.escape(c['htmlchars'])
        if c['lineend']:
            return '<br>'
        elif c['space']:
            t = m.group().replace('\t', '&nbsp;' * tabstop)
            t = t.replace(' ', '&nbsp;')
            return t
        elif c['space'] == '\t':
            return ' ' * tabstop
        else:
            url = m.group('protocal')
            if url.startswith(' '):
                prefix = ' '
                url = url[1:]
            else:
                prefix = ''
            last = m.groups()[-1]
            if last in ['\n', '\r', '\r\n']:
                last = '<br>'
            return "%s<a target='_blank' href='%s'>%s</a>%s" % (prefix, url, url, last)
    return re.sub(re_string, do_sub, text)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def generate_random_string(length=6, char_parts=None):
    """
    生成随机字符串

    :param length: 字符串长度
    :param char_parts: 字符串组成部分
    :return: 随机字符串
    """
    if char_parts is None:
        char_parts = [
            string.ascii_uppercase,  # ABC...
            string.ascii_lowercase,  # abc...
            "".join([c for c in string.punctuation if c not in ['"', "'"]]),  # ^&*...
            string.digits            # 123...
        ]

    results = []
    for i in range(length):
        chars = char_parts[(i % len(char_parts))]
        results.append("".join(random.sample(chars, 1)))
    random.shuffle(results)
    return "".join(results)


def generate_random_digits(length=6):
    """
    Generate random digits

    :return: string
    """
    return generate_random_string(length, char_parts=[string.digits])


def sizeof_fmt(num, suffix='B'):
    """
    Human-readable file size

    Ref: https://stackoverflow.com/a/1094933/7452313

    :param num: file size in bytes
    :param suffix:
    :return: string
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)
