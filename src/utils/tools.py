# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import cgi
import re


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
