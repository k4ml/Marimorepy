#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, MARIMORE LLC Tokyo, Japan.
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
#   *   Neither the name of the MARIMORE LLC nor the names of its contributors 
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
__date__        = "$LastChangedDate: 2009-10-12 01:36:53 +0900 (月, 12 10月 2009) $"
__version__     = "$LastChangedRevision: 23 $"

import sys

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

    except Exception, e:
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

if __name__ == '__main__':
    log_syslog("test", "test test")
    import_object('test')