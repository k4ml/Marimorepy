#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, MARIMORE Inc Tokyo, Japan.
# Contributed by 
#       Affandi Mustapa <affandi@marimore.co.jp>
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
Paypal billing module

Contains classes and functions to process Paypal requests
G{importgraph}
"""

__date__        = "$LastChangedDate$"
__version__     = "$LastChangedRevision$"

from mamopublic import common
import urllib, urllib2

from mamopublic.utils.helpers import log_syslog

class PaypalAPI(common.BaseClass):
    """
    This class enacapulates utilities to verify and use IPN messages from Paypal
    """

    _PP_CALLBACK_TEST_URL   = "https://www.sandbox.paypal.com/cgi-bin/webscr"
    _PP_CALLBACK_URL        = "https://www.paypal.com/cgi-bin/webscr"

    def __init__(self, ipn_data, config={}):
        """

        @type ipn_data: dictionary
        @param ipn_data: The ipn data i.e django's request.POST.copy() 
        """

        # Configurations are passed to the class but this class should
        # not be connected to django directly
        self._config = config
        self._ipn_data = ipn_data

        if self._config.get('paypal_prod_flag', False):
            self._test_flag = False
        else:
            # If flag is not set, default is in testing
            self._test_flag = True

    def verify_ipn(self):
        """
        Verifies that the IPN is authentic

        @return: True if the paypal ipn was verified succesfully
        """

        if self._test_flag:
            _PP_URL = self._PP_CALLBACK_TEST_URL
        else:
            _PP_URL = self._PP_CALLBACK_URL

        ipn_data = self._ipn_data
        ipn_data['cmd'] = "_notify-validate"

        tmp_ipn_data = {}
        for k in ipn_data.keys():
            tmp_ipn_data[k] = ipn_data[k].encode(ipn_data['charset'])

        params = urllib.urlencode(tmp_ipn_data)

        req = urllib2.Request(_PP_URL, params)
        req.add_header("Content-type", "application/x-www-form-urlencoded")

        try:
            response = urllib2.urlopen(req)
            status = response.read().strip()
        except IOError:
            return -100

        if status == "VERIFIED":
            return 0

        return -1

    def check_seller_email(self):

        if self._ipn_data['receiver_email'] == self._config['paypal_seller_email']:
            return True

        return False

