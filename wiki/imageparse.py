import os, sys, re
import urllib
import string

IMAGES_DIR = "images"

def parse(file):
	baseName = os.path.basename(file)
	newStr = ""
	changes = False
	with open(file, 'r') as f:
		str = f.read()

		if "imgur" in str:
			print "%s contains imgur" % baseName

		match = re.search("\!\[.*\]\((.*)\)", str)
		lastMatch = match

		while match:
			imgURL = match.group(1)
			imgName = os.path.basename(imgURL)
			newURL = os.path.join(IMAGES_DIR, imgName)
			
			if os.path.exists(newURL):
				pass
				#print "image already exists: %s" % (match.group(0))
			else:
				urllib.urlretrieve(imgURL, newURL)
				changes = True

			newStr += str[:match.start(1)]
			newStr += newURL
			str = str[match.end(1):]
			lastMatch = match
			match = re.search("\!\[.*\]\((.*)\)", str)

		if lastMatch:
			newStr += str

	#if we found some matches
	if newStr:
		with open(file, 'w') as f:
			f.write(newStr)

	return len(newStr)!=0 and changes

path = "."
files = [p for p in os.listdir(path) if p.lower().endswith('.md')]

for f in files:
	ret = parse(f)
	if ret:
		print "updated %s" % f