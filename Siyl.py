#!/usr/bin/python
# SqlI In You Logs
# Basic sqli DeCruncher

import sys,urllib,re,getopt
VER = '0.0c'

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
	print ' -n : Disable URL encoding of cr lf'

# Programme initialisation
def init(argv):
	global _pipemode
	_pipemode = False
	global _ojoin
	_ojoin = True 
	global _ochar
	_ochar = True
	global _ourld
	_ourld = True
	global _okeepcr
	_okeepcr = True

	try:
		opts, args = getopt.getopt(argv,"hjcunp")
	except getopt.GetoptError:
		help()
		sys.exit(2)

	# Parse line option
	for opt, arg in opts:
        # Help requested
		if opt == '-h':
			help()
			sys.exit()
		if opt in '-j':
			_ojoin = False
		if opt in '-c':
			_ochar = False
		if opt in '-u':
			_ourld = False
		if opt in '-n':
			_okeepcr = False
		# Pipemode requested
		if opt in '-p':
			_pipemode = True

	# return all other parameter (filelist)	
	return (args)

def clean(line):
	# Cleanup end crlf
	line = line.rstrip('\n')
	line = line.rstrip('\r')

	# Url Decode
	if _ourld:
		line = urllib.unquote(line).decode('utf-8')
		# Keep 0A and 0D Encoded
		if _okeepcr:
			line = line.replace(b"\n", "%0D")
			line = line.replace(b"\r", "%0A")
		
	# Convert Charcode to ASCII
	if _ochar:
		line2 = ""
		pattern = re.compile(r"(CHR\([0-9]{1,3}\))")
		patterchr = re.compile(r"CHR\(([0-9]{1,3})\)")
		for fields in pattern.split(line):
			if 'CHR(' in fields:   # String a convertir
				for fchar in patterchr.split(fields):
					if fchar <> '':
						line2 = line2+chr(int(fchar))
			else:
				line2 = line2+fields
		line = line2

	# Remove Join for lisibility
	if _ojoin:
		line = line.replace('||','')

	return(line)

# Main program loop
def main(argv):

	filelist = init(argv)

	print _ojoin
	print _pipemode
	if _pipemode == True:
		print 'proute'
		while True:
			print 'proute'
			line = sys.stdin.readline()
			if not line:
				break
			print clean(line)
	else:
		for file in filelist:			
			# Default mode is file
			# test if file exists
			f = open(file, 'r' )
			# Main loop
			while True:
				line = f.readline()
				#Si fin d'input arret
				if not line:
					break

				# Sinon....
				print clean(line)


if __name__ == "__main__":
	main(sys.argv[1:])
