#!/bin/bash

openssl req -x509 -newkey rsa:2048 -keyout $SSL_KEY_PATH/transc.key \
    -out $SSL_CERT_PATH/transc.crt -sha256 -days 365 -nodes -subj \
    "/C=MA/ST=BG/L=BG/O=Transc/OU=Net/CN=www.Transc-Net.com" > /dev/null 2>&1

nginx -g "daemon off;"