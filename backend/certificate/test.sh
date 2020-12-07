#!/bin/bash
KCNAME=new
openssl genrsa 2048 > $KCNAME.key
chmod 400 $KCNAME.key
openssl req -new -x509 -nodes -sha1 -days 365 -key $KCNAME.key > $KCNAME.crt
