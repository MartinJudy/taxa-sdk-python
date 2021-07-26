from __future__ import print_function

import binascii
import os
from .taxa_request import TaxaRequest

def get_template():
    template = os.path.abspath(os.path.join(__file__, "../browser_ui.html"))
    with open(template) as f:
        return f.read()

def make_nice(bin):
    return binascii.b2a_base64(bin)[:-1].decode()

def make_html(verbose):
    r = TaxaRequest("browserUI.json", verbose=verbose)
    r.ip = "52.138.6.109"
    r.force_attestation()

    vars = (
        'var client_cert = "%s";\n' % make_nice(r.key_manager.client_cert) +
        '      var client_key = "%s";\n' % make_nice(r.key_manager.client_key) +
        '      var master_key = "%s";\n' % make_nice(r.key_manager.master_key_key) +
        '      var master_key_iv = "%s";\n' % make_nice(r.key_manager.master_key_iv) +
        '      var ip = "' + r.ip + '";\n'
    )

    return [
        get_template().replace("{{{ vars }}}", vars),
        make_nice(r.key_manager.client_pubkeyhash).replace("/", "") # to make valid filename
    ]

def write_browser_ui():
    html, pubkeyhash = make_html(verbose=False)
    filename = "/tmp/taxa_%s.html" % pubkeyhash[:8]

    with open(filename, 'w') as f:
        f.write(html)

    return filename

if __name__ == "__main__":
    print(write_browser_ui())
