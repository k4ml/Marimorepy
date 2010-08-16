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
This module defines commonly used utility code for working with files
"""

__author__      = "Iqbal Abdullah <iqbal@marimore.co.jp>"
__date__        = "$LastChangedDate$"
__version__     = "$LastChangedRevision$"

import random
import time
import string

def generate_random_filename(randlen=2, suffix=None):
    """
    Generates a random string with a specified prefix, useful for generating
    random filenames. No two filenames will be the same if executed on the same machine

    @type  suffix: string or None
    @param suffix: The suffix to append at the end of the filename, i.e xxxx.gif or xxxx.html
                   Default is None.
    @type  randlen: integer
    @param  randlen: The length of the random prefix for the filename. Defaults to 2 with a maximum of 7
    @rtype: string
    @return: The random filename
    """

    try:
        int(randlen)
        if randlen > 7:
            randlen = 7
    except:
        randlen = 2

    if suffix:
        return "%s%s.%s" % ( "".join(random.sample(string.digits + string.ascii_lowercase, randlen)), int(time.time()), suffix.strip() )
    else:
        return "%s%s" % ( "".join(random.sample(string.digits + string.ascii_lowercase, randlen)), int(time.time()) )


if __name__ == '__main__':

    print generate_random_filename()
    print generate_random_filename("jpg")
    print generate_random_filename(7,"jpg")
    print generate_random_filename(10,"jpg")
    print generate_random_filename(5,"jpg")

