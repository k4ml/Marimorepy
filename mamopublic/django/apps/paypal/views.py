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
These are views for Paypal IPN listener
"""

__date__        = "$LastChangedDate$"
__version__     = "$LastChangedRevision$"

from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import HttpResponse, render_to_response, get_object_or_404
from django.conf import settings
import urllib, urllib2

from mamopublic.utils.helpers import log_syslog
from mamopublic.utils.helpers import import_object
from mamopublic.dev.debug import logger

from models import PaypalPayments
from paypalapi import PaypalAPI


def ipn(request):
    """
    These are the required variables in settings.py:

    PAYPAL_SELLER_EMAIL
    PAYPAL_PROD_FLAG
    PAYPAL_PN_FUNCTION
    PAYPAL_LOG_FILE
    """

    if request.method == "POST":

        # Before we do anything, set the encoding for the request
        request.encoding = request.POST['charset']

        try:
            ipn_data = request.POST.copy()

            log_string = "NOTICE: Received IPN from Paypal txn_id:%s" % (ipn_data.get('txn_id', ""))
            log_syslog("paypal.views", log_string, facility="LOG_LOCAL2")

            # Before we do anything else, log the IPN data into the log file
            # It is important to have the original untouched IPN data logged first for debugging
            logger("%s" % (ipn_data), settings.PAYPAL_LOG_FILE)

            # PAYPAL_SELLER_EMAIL is critical to have, so I purposely do not check for exceptions here
            # let the errors come out noisily if we don't have this in settings.py
            paypal_seller_email = settings.PAYPAL_SELLER_EMAIL
            try:
                paypal_prod_flag = settings.PAYPAL_PROD_FLAG
            except:
                paypal_prod_flag = True

            config = {}
            config['paypal_prod_flag'] = paypal_prod_flag
            config['paypal_seller_email'] = paypal_seller_email

            ppapi_object = PaypalAPI(ipn_data, config)

            errcode = ppapi_object.verify_ipn()

            if errcode == -1:
                # Return OK and do not process further
                log_string = "ERROR: IPN from Paypal failed callback verification txn_id:%s" \
                             % (ipn_data.get('txn_id', ""))
                log_syslog("paypal.views", log_string, facility="LOG_LOCAL2")
                return HttpResponse("OK")

            elif errcode == -100:
                # Connecting to Paypal caused an IO Error. Ask Paypal to resend
                log_string = "ERROR: Paypal verification IOError txn_id:%s" % (ipn_data.get('txn_id', ""))
                log_syslog("paypal.views", log_string, facility="LOG_LOCAL2")
                return HttpResponseServerError()

            if not ppapi_object.check_seller_email():
                # Return OK and do not process further
                log_string = "ERROR: IPN from Paypal had invalid seller email txn_id:%s" \
                             % (ipn_data.get('txn_id', ""))
                log_syslog("paypal.views", log_string, facility="LOG_LOCAL2")
                return HttpResponse("OK")

            if PaypalPayments.objects.filter(txn_id=ipn_data.get('txn_id', ""), payment_status="Completed").count() != 0:
                log_string = "ERROR: IPN from Paypal is already complete txn_id:%s" % (ipn_data.get('txn_id', ""))
                log_syslog("paypal.views", log_string, facility="LOG_LOCAL2")
                return HttpResponse("OK")

            txn_type = ipn_data.get('txn_type', "").lower().strip()

            # ipn is verified. Ok, next we must:
            # 1. Write ipn data to log file first
            # 2. Process ipn data againts payment function
            # 3. If payment function is ok, add data to models

            ############# HOOK ##################
            payment_process_function = import_object(settings.PAYPAL_PN_FUNCTION)
            errcode = payment_process_function(ipn_data)
            ############# HOOK ##################

            if errcode == 111:
                # Ask paypal to send the IPN again later
                return HttpResponseServerError()
            elif errcode != 0:
                log_string = "ERROR: Paypal failed payment processing txn_id:%s errcode:%s" \
                             % (ipn_data.get('txn_id', ""), errcode)
                log_syslog("paypal.views", log_string, facility="LOG_LOCAL2")
                return HttpResponse("OK")
            else:
                # errcode == 0
                log_string = "NOTICE: Paypal processing success txn_id:%s" % (ipn_data.get('txn_id', ""))
                log_syslog("paypal.views", log_string, facility="LOG_LOCAL2")

            try:
                # treat transaction ids without txn_id as a new transaction; 
                # subscription signups do not have txn_id
                txn_id = ipn_data.get('txn_id', "")
                if txn_id == "":
                    p1 = PaypalPayments()
                else:
                    p1 = PaypalPayments.objects.get(txn_id=txn_id)
            except:
                p1 = PaypalPayments()

            for index,item in enumerate(ipn_data):                
                p1.__dict__[item] =  ipn_data[item]
            p1.save()

        except Exception, e:
            # Ask paypal to send the IPN again later
            log_string = "ERROR: Exception caught processing txn_id:%s exception:%s" \
                         % (ipn_data.get('txn_id', ""), e)
            log_syslog("paypal.views", log_string, facility="LOG_LOCAL2")
            return HttpResponseServerError()

        return HttpResponse("OK")

    else:
        # Not a POST request. Ignore
        return HttpResponse("OK")

