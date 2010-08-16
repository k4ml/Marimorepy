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
This module defines commonly used utility code for working with strings
"""

__author__      = "Iqbal Abdullah <iqbal@marimore.co.jp>"
__date__        = "$LastChangedDate$"
__version__     = "$LastChangedRevision$"

import string

def is_alnum(str, okchars=None):
    """
    Checks if the given string only contains alnum characters (i.e like string.alnum) but allows you
    to also include specific characters which you want to allow

    @type str: string
    @param str: The string we want to check for
    @type okchars: string
    @param okchars: A string of ok characters, besides the normal alnum chars (i.e hyphens)
    @return: True if the given string only contains alnum and allowed characters
    """

    if okchars:
        _oklist = list(string.ascii_letters + string.digits) + list(okchars)
    else:
        _oklist = list(string.ascii_letters + string.digits)

    str_list = list(str)
    for s in str_list:
        if s not in _oklist:
            return False

    return True


if __name__ == '__main__':

    print is_alnum("bauAhfg345%")
    print is_alnum("bauAhfg345%!@", "!@%")
    print is_alnum("bauAhfg345%!@", "!%")
    print is_alnum("bauAhfg345")
    print is_alnum("漢字abc")

