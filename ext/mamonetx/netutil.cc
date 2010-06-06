/*
# Copyright (c) 2009, MARIMORE Inc Tokyo, Japan.
# Contributed by 
#       Iqbal Abdullah <iqbal@marimore.co.jp>
# All rights reserved.
#
# Part of this setup script was taken from Django-1.1 setup.py. All rights reserved.
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
*/

extern "C" {
    #include "Python.h"

    // For libspf
    #include "spf.h"
}

static PyObject* email_has_valid_spf(PyObject *self, PyObject *args)
{
    SPF_BOOL use_trusted = SPF_FALSE;
    SPF_BOOL use_guess   = SPF_FALSE;

    const char* peer_ip;
    const char* email_address;
    const char* helo_host;

    unsigned int spf_results = 0;

    if (!PyArg_ParseTuple(args, "sss", &helo_host, &peer_ip, &email_address)) 
        return NULL;

    peer_info_t *pinfo = NULL;
    if ( (pinfo = SPF_init(helo_host, peer_ip, NULL, NULL, NULL, use_trusted, use_guess)) != NULL) 
    {
        SPF_smtp_helo(pinfo, helo_host);
        SPF_smtp_from(pinfo, email_address);
        SPF_policy_main(pinfo);

        if (pinfo->RES == SPF_PASS) {
            spf_results = 1;
        }
    }

    SPF_close(pinfo);
    if (spf_results) Py_RETURN_TRUE;

    Py_RETURN_FALSE;
}


static PyMethodDef UtilMethods[] = {
        // Define the methods for the module here

        {"email_has_valid_spf",  email_has_valid_spf, METH_VARARGS, 
            "Checks if an ip and email address has a valid spf"},
        {NULL, NULL, 0, NULL}        /* Sentinel */
};


/*
The initialization function for the module must be named initname, where name is the name of
the module, and should be the only non-static item defined in the module file
*/

PyMODINIT_FUNC initmamonetx()
{
    (void) Py_InitModule("mamonetx", UtilMethods);
}

