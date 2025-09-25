#!/bin/sh

source=$1
fname=$(basename $source)

cat $source | envsubst > /usr/share/nginx/html/$fname && nginx -g 'daemon off;'
