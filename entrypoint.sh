#!/bin/bash
set -e
SUPERVISOR_PROGRAM=${PROGRAM:-supervisor} # default value is supervisor

echo "Replacing supervisord.conf"
cp setup/main_supervisord.conf /etc/supervisor/supervisord.conf || exit 1

echo "Copying supervisor program conf"
cp "setup/${SUPERVISOR_PROGRAM}.conf" /etc/supervisor/conf.d/ || exit 1

echo "Replacing PROGRAM with ${SUPERVISOR_PROGRAM}"
sed -i -e "s#PROGRAM#$SUPERVISOR_PROGRAM#g" /etc/supervisor/supervisord.conf || exit 1

exec supervisord -c /etc/supervisor/supervisord.conf
