#!/usr/bin/python
# SqlI In You Logs
# Basic sqli DeCruncher

import sys,urllib,re,getopt
VER = '0.0a'

# Help 
def help():
	print 'Siyl - v'+VER+' - Decode Sqli in your logs - (c) Thanat0s 2012'
	print ''
	print 'Usage :'
	print 'Piped  : zcat mylogs.gz | Siyl -p'
	print 'Direct : Siyl -i [FILE]'
	print ''
	print 'Switches:'
	print ' -h for Help'
	print ' -p for PipeMode or -i [FILE] for Filemode'
	print ' -j : Disable \'||\' joining'
	print ' -c : Disable chr(xx) decoding'
	print ' -u : Disable URL decoding'

# Main program loop
def main(argv):
	global _pipemode
	_pipemode = 0
	global _filemode
	_filemode = 0
	global _ojoin 
	_ojoin = 1	
	global _ochar
	_ochar = 1
	global _ourld
	_ourld = 1

	try:
		opts, args = getopt.getopt(argv,"hpjcui:",["ifile="])
	except getopt.GetoptError:
		help()
		sys.exit(2)

	for opt, arg in opts:
		# Help requested
		if opt == '-h':
			help()
			sys.exit()
		print 'prite'
		if opt in '-j':
			_ojoin = 0
		if opt in '-c':
			_ochar = 0
		if opt in '-u':
			_ourld = 0
		# Pipemode requested
		if opt in '-p':
			_pipemode = 1	
		# file requested
		elif opt in ("-i", "--ifile"):
			_filemode = 1
			_inputfile = arg
			f = open(_inputfile, 'r' )

	# if no mode choosen halt
	if (_pipemode + _filemode) <> 1:
		print 'Error: No mode choosen'
		help()
		sys.exit()


	# Main loop
	while True:
		if _pipemode:
			line = sys.stdin.readline()
		else:
			line = f.readline()
		#Si fin d'input arret
		if not line:
			break

		# Sinon....

		# Url Decode
		if _ourld:
			line = urllib.unquote(line).decode('utf-8')

		# Charcode
		if _ochar:
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
		if _ojoin:
			line = line.replace('||','')

		print line.rstrip('\n')


if __name__ == "__main__":
	main(sys.argv[1:])
