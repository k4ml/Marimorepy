#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, MARIMORE Inc Tokyo, Japan.
# Contributed by 
#       Iqbal Abdullah <iqbal@marimore.co.jp>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, 
# are permitted provided that the following conditions are met:
#
#   *   Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer.
#   *   Redistributions in binary form must reproduce the above copyright notice, 
#       this list of conditions and the following disclaimer in the documentation 
#       and/or other materials provided with the distribution.
#   *   Neither the name of the MARIMORE Inc nor the names of its contributors 
#       may be used to endorse or promote products derived from this software 
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
This module defines helper functions
"""

__author__      = "Iqbal Abdullah <iqbal@marimore.co.jp>"
__date__        = "$LastChangedDate$"
__version__     = "$LastChangedRevision$"

import sys, datetime
import inspect

def import_object(qualified_name):
    """
    import_object() will return the module/function/class which is specified
    in qualified_name

    @type qualified_name: string
    @param qualified_name: The fully qualified package path to the target
    @rtype: object or None
    @return: An object to the target module/function/class or None if an exception
             occurred
    """

    parent_namespace = ".".join(qualified_name.split(".")[:-1])
    target_namespace = qualified_name.split(".")[-1]

    if parent_namespace == "":
        # This is the top module
        parent_namespace = target_namespace

    try:
        __import__(parent_namespace)
        m = sys.modules[parent_namespace]
        mod = getattr(m, target_namespace)
        return mod

    except (Exception) as e:
        print "Exception occurred 02: import_object(): %s" % (e)
        return None


def log_syslog(ident, message, priority="LOG_NOTICE", facility="LOG_USER"):
    """
    Writes log messages via the system syslog(). This is for UNIX based systems only.

    @type facility: string
    @param facility: The facility to be used. It can be one of these:
        1. LOG_KERN
        2. LOG_USER
        3. LOG_MAIL
        4. LOG_DAEMON
        5. LOG_AUTH
        6. LOG_LPR
        7. LOG_NEWS
        8. LOG_UUCP
        9. LOG_CRON 
        10. LOG_LOCAL0 to LOG_LOCAL7
    By default it will be LOG_USER

    @type priority: string
    @param priority: The priority of the message, which can be one of these:
        1. LOG_EMERG
        2. LOG_ALERT
        3. LOG_CRIT
        4. LOG_ERR
        5. LOG_WARNING
        6. LOG_NOTICE
        7. LOG_INFO
        8. LOG_DEBUG
    By default it is LOG_NOTICE

    @type ident: string
    @param ident: The prepended indent for your message. Usually this is the filename.
    @type message: string
    @param message: The message you want to log to
    """

    try:
        import syslog
    except:
        return -1

    if facility == "LOG_KERN":
        fac = syslog.LOG_KERN
    elif facility == "LOG_MAIL":
        fac = syslog.LOG_MAIL
    elif facility == "LOG_DAEMON":
        fac = syslog.LOG_DAEMON
    elif facility == "LOG_AUTH":
        fac = syslog.LOG_AUTH
    elif facility == "LOG_LPR":
        fac = syslog.LOG_LPR
    elif facility == "LOG_NEWS":
        fac = syslog.LOG_NEWS
    elif facility == "LOG_UUCP":
        fac = syslog.LOG_UUCP
    elif facility == "LOG_CRON":
        fac = syslog.LOG_CRON
    elif facility[:9] == "LOG_LOCAL":
        if facility[9] == "0":
            fac = syslog.LOG_LOCAL0
        elif facility[9] == "1":
            fac = syslog.LOG_LOCAL1
        elif facility[9] == "2":
            fac = syslog.LOG_LOCAL2
        elif facility[9] == "3":
            fac = syslog.LOG_LOCAL3
        elif facility[9] == "4":
            fac = syslog.LOG_LOCAL4
        elif facility[9] == "5":
            fac = syslog.LOG_LOCAL5
        elif facility[9] == "6":
            fac = syslog.LOG_LOCAL6
        elif facility[9] == "7":
            fac = syslog.LOG_LOCAL7
        else:
            # There's only 0 to 7
            fac = syslog.LOG_USER
    else:
        fac = syslog.LOG_USER

    if priority == "LOG_EMERG":
        prio = syslog.LOG_EMERG
    elif priority == "LOG_ALERT":
        prio = syslog.LOG_ALERT
    elif priority == "LOG_CRIT":
        prio = syslog.LOG_CRIT
    elif priority == "LOG_ERR":
        prio = syslog.LOG_ERR
    elif priority == "LOG_WARNING":
        prio = syslog.LOG_WARNING
    elif priority == "LOG_INFO":
        prio = syslog.LOG_INFO
    elif priority == "LOG_DEBUG":
        prio = syslog.LOG_DEBUG
    else:
        prio = syslog.LOG_NOTICE

    syslog.openlog(ident, 0, fac)
    syslog.syslog(prio, message)

def log_syslogn(message, ident=None, priority="LOG_NOTICE", facility="LOG_USER"):
    """
    Shortcut to log to LOCALn. The function signature should be similar to log_syslog
    except that message is swapped to be the first so indent would be optional.
    If indent is None, use inspect module to get the calling function name.
    """
    def get_ident(frame):
        frame_info = inspect.getframeinfo(frame[0])

        if 'self' in frame[0].f_locals:
            instance = frame[0].f_locals['self']
        else:
            instance = None

        mod = inspect.getmodule(frame[0])
        filename, lineno, function, code_context, index = frame_info

        if instance:
            ident = '%s.%s.%s()' % (mod.__name__, instance.__class__.__name__,
                                    function.strip())
        else:
            if mod.__name__ == '__main__':
                modname = filename
            else:
                modname = mod.__name__
            ident = '%s.%s()' % (modname, function.strip())

        return ident

    if not ident:
        frame = None
        frame_info = None
        try:
            frame = inspect.stack()[2]
            ident = get_ident(frame)
        except Exception:
            ident = ''
        finally:
            del frame
            del frame_info

    # split message by newline and then joining it back, removing any tabs or
    # space that resulted from indentation. Log message always in single line.
    messages = [line.strip() for line in message.split()]
    message1 = " ".join(messages)

    log_syslog(ident, message1, priority, facility=facility) 

def log_syslog0(message, ident=None, priority="LOG_NOTICE", facility="LOG_LOCAL0"):
    log_syslogn(message, ident, priority, facility=facility) 

def log_syslog1(message, ident=None, priority="LOG_NOTICE", facility="LOG_LOCAL1"):
    log_syslogn(message, ident, priority, facility=facility) 

def log_syslog2(message, ident=None, priority="LOG_NOTICE", facility="LOG_LOCAL2"):
    log_syslogn(message, ident, priority, facility=facility) 

def log_syslog3(message, ident=None, priority="LOG_NOTICE", facility="LOG_LOCAL3"):
    log_syslogn(message, ident, priority, facility=facility) 

def log_syslog4(message, ident=None, priority="LOG_NOTICE", facility="LOG_LOCAL4"):
    log_syslogn(message, ident, priority, facility=facility) 

def uniqify_list(seq, idfun=None): 
    """
    Uniqify a list while preserving order. i.e

    If you have a list such as [1,2,2,2,3,4,5,6,6,6,6] uniqify_list() while 
    return [1,2,3,4,5,6]

    You can also specify a function to transform the data, i.e

    >>> a=list('ABeeE')
    >>> uniqify_list(a)
    ['A','B','e','E']
    >>> uniqify_list(a, lambda x: x.lower())
    ['A','B','e'] 

    Taken from http://www.peterbe.com/plog/uniqifiers-benchmark

    @type seq: list
    @param seq: The list which you want to uniqify 
    @type idfun: a function, defaults to None
    @param idfun: A function which you want to process the data with
    @rtype: list
    @return: An list which has been uniqified
    """

    if idfun is None:
        def idfun(x): return x

    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)

    return result

def calculate_time(base_time, diff_seconds, reverse=False): 
    """
    Calculates a new time if you add diff_seconds to base_time

    @type base_time: datetime object
    @param base_time: The base time which you want to do the calculation on
    @type diff_seconds: signed int
    @param diff_seconds: The time difference in seconds. Use a negative value if the time is in the past
    @type reverse: bool
    @param reverse: Reverse calculation; Instead of adding diff_seconds to base_time, you do deduction.
                    This is useful in cases where you have the localtime and the delta but you want to
                    find the UTC.
    @rtype: datetime object
    @return: A datetime object representing the calculated time
    """

    diff_time = datetime.timedelta(seconds=diff_seconds)
    if reverse:
        new_time = base_time - diff_time
    else:
        new_time = base_time + diff_time
    return new_time

if __name__ == '__main__':
    #log_syslog("test", "test test")
    #import_object('test')
    print uniqify_list(list('123123454324332ABCAABCabcaabcrt'))
    print calculate_time(datetime.datetime.now(), -60)
    print calculate_time(datetime.datetime.now(), -60, True)
