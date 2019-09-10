# heyujs
HeyuJS is a web application and API that wraps heyu X10 command line utility for main fucntions.

It is designed as a single page application using Google AngularJS (1.x) and Anguar material calling a Python-Flask API served by UWSGI/python3 engine.

The default provided installation configure NGINX o serve the client JS application and proxy API requests to UWSGI service through a local unix socket.

## Installation

prerequisites for install with provided sript
- Ubuntu 18.04
- sudo rights for your current user

packages:
- python3
- nginx-full
- uwsgi-plugin-python3

download zip from github and:
- cd heyujs/deploy
- install.sh

will install and start the application into 

'''/var/www/html/heyujs'''

## access

Access through http://yourserver/heyujs

HeyuJS is responsive and supports wide screens and smartphones sizes.

## configure

A fake configuration is provided. The application allows to manage your whole configuration, but you can provide your own x10config and x10.shed files into deploy directory before to install.

## security

The application do not implement any flow encryption (HTTPS) not authentication nor right mechanism.
Use the reverse proxy (NGINX) in order to implement these security features.
For right management, admin / user rights isolation is in API future plans and will rely on reverse proxy generated request headers transmitted to the API.

## status

This application is in draft mode

Todo:
- user/admin right management in API
- Ansible playbook deployer

