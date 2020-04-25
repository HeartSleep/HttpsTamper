# -*- coding: utf-8 -*-
import frida, sys, re, sys, os
from subprocess import Popen, PIPE, STDOUT
import codecs, time

#需要重启应用
rdev = frida.get_usb_device()
front_app = rdev.get_frontmost_application()
print (front_app)
jscode=open('trace_call.js').read()
process = frida.get_usb_device().attach(front_app.identifier)
script = process.create_script(jscode)
script.load()
sys.stdin.read()