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
These are models for Paypal billing
"""

__date__        = "$LastChangedDate$"
__version__     = "$LastChangedRevision$"

from django.db import models

class PaypalPayments(models.Model):

    # Transaction information
    # No txn_id for subscriptions; Make blank=True
    txn_id = models.CharField(max_length=255, blank=True)
    txn_type = models.CharField(max_length=255)
    parent_txn_id = models.CharField(max_length=255)        # the parent id for refund, reversal or canceled transactions
    notify_version = models.CharField(max_length=255)
    test_ipn = models.CharField(max_length=255)
    resend = models.CharField(max_length=255)
    charset = models.CharField(max_length=255)
    verify_sign = models.CharField(max_length=255)

    # Advanced and custom information		
    custom = models.CharField(max_length=255, blank=True)

    # Merchant information		
    receiver_email = models.CharField(max_length=255)
    receiver_id = models.CharField(max_length=255, blank=True)
    residence_country = models.CharField(max_length=2)

    # Payment information
    payment_type = models.CharField(max_length=255)
    payment_date = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=255)
    invoice = models.CharField(max_length=255, blank=True)
    memo = models.CharField(max_length=255, blank=True)

    # Product information
    item_number = models.CharField(max_length=255, blank=True)

    # Payment financials
    mc_currency = models.CharField(max_length=255, blank=True)
    mc_gross = models.DecimalField(max_digits=12, decimal_places=3, null=True)     # 1 billion with 3 digits
    mc_fee = models.DecimalField(max_digits=12, decimal_places=3, null=True)       # 1 billion with 3 digits
                    
    #Shipping and handling
    mc_shipping = models.DecimalField(max_digits=12, decimal_places=3, null=True)  # 1 billion with 3 digits
    tax = models.DecimalField(max_digits=12, decimal_places=3, null=True)          # 1 billion with 3 digits

    #Refunds/reversals		
    reason_code = models.CharField(max_length=255)
                   
    #Pending payments
    pending_reason = models.CharField(max_length=255, blank=True)
                    
    #Buyer information
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    payer_status = models.CharField(max_length=255)
    payer_email = models.CharField(max_length=255)
    payer_id = models.CharField(max_length=255)

    address_status = models.CharField(max_length=255, blank=True)
    address_country = models.CharField(max_length=255, blank=True)
    address_city = models.CharField(max_length=255, blank=True)
    address_country_code = models.CharField(max_length=2, blank=True)
    address_name = models.CharField(max_length=255, blank=True)
    address_state = models.CharField(max_length=255, blank=True)
    address_street = models.CharField(max_length=255, blank=True)
    address_zip = models.CharField(max_length=255, blank=True)
    contact_phone = models.CharField(max_length=255, blank=True)

    #Recurring payments
    subscr_id = models.CharField(max_length=255, blank=True)

    #Django custom: Time you received this ipn for the first time
    ipn_received_time     = models.DateTimeField(auto_now=False, auto_now_add=True)
    #Django custom: Time you received an status change for this ipn
    ipn_changed_time     = models.DateTimeField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return self.txn_id
