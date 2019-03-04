#!/usr/bin/env python
import ssl
import OpenSSL.crypto as crypto

def inspect(host, port):
    raw_cert = ssl.get_server_certificate((host, port))
    x509 = crypto.load_certificate(crypto.FILETYPE_PEM, raw_cert)
    print(x509.get_notAfter())

if __name__ == "__main__":
    inspect("baidu.com", 443)
