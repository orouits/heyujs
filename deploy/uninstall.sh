#!/bin/bash
srcdir=$(dirname $(dirname $(readlink -f ${0})))
homedir=/var/www/html/heyujs
logdir=/var/log/heyujs
echo "Source dir: ${srcdir}"
echo "Home dir: ${homedir}"
echo "Log dir: ${logdir}"

sudo systemctl stop heyujs
sudo systemctl disable heyujs
sudo rm /etc/systemd/system/heyujs.service
sudo rm -rf "${logdir}"

sudo rm /etc/nginx/sites-enabled/heyu.conf
sudo systemctl restart nginx
sudo rm -rf "${homedir}"

