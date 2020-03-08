#!/bin/bash
srcdir=$(dirname $(dirname $(readlink -f ${0})))
homedir=/var/www/html/heyujs
logdir=/var/log/heyujs
echo "Source dir: ${srcdir}"
echo "Home dir: ${homedir}"
echo "Log dir: ${logdir}"

# clean

sudo systemctl stop heyujs
sudo systemctl disable heyujs
sudo rm -rf "${logdir}"

sudo rm -rf "${homedir}"

# install

sudo cp -r "${srcdir}" "${homedir}"
sudo cp ${srcdir}/deploy/x10* "${homedir}/api"
sudo chown www-data:www-data -R "${homedir}"

sudo cp ${srcdir}/deploy/heyujs.service /etc/systemd/system
sudo mkdir "${logdir}"
sudo chown www-data:www-data "${logdir}"
sudo systemctl enable heyujs
sudo systemctl start heyujs

sudo cp ${srcdir}/deploy/heyu.conf /etc/nginx/sites-enabled/
sudo systemctl restart nginx
