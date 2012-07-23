#!/usr/bin/python
# SqlI In You Logs
# Basic sqli DeCruncher

import sys
import urllib
import re

while True:
	line = sys.stdin.readline()
	#Si fin d'input arret

	if not line:
		break

	# Sinon....

	# Url Decode
	line = urllib.unquote(line).decode('utf-8')

	# Charcode
	line2 = "" 
	pattern = re.compile(r"(CHR\([0-9]{1,3}\))")
	patterchr = re.compile(r"CHR\(([0-9]{1,30})\)")
	for fields in pattern.split(line):
		if 'CHR(' in fields:   # String a convertir
			for fchar in patterchr.split(fields):
				if fchar <> '':
					line2 = line2+chr(int(fchar))
		else:
			line2 = line2+fields

	line = line2
	# Join
	line = line.replace('||','')

	print line.rstrip('\n')
