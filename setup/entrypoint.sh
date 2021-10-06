#!/bin/bash

#export COUNT_FILES=$(ls -A /anfisa/a-setup/ | wc -l)
#if [ ${COUNT_FILES} -le 2 ] ; then
#    mkdir -p /anfisa/a-setup/{data,logs,vault,export/work,ui}
#fi
#
#if [ ! -z ${ANFISA_COORD_HOST+z} ] && [ ! -z ${ANFISA_ROUTER_HOST+z} ] && [ ! -z ${ANFISA_MONGO_HOST+z} ] ;
#then
#    sed "s#anfisa-test-coordinator#${ANFISA_COORD_HOST}#g" /anfisa/anfisa.json | sed "s#anfisa-test-router#${ANFISA_ROUTER_HOST}#g" | sed "s#anfisa-test-mongo#${ANFISA_MONGO_HOST}#g" -  > /anfisa/anfisa.json
#fi
#
#exec "$@"

ls
