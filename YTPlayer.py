#!/usr/bin/python3

import subprocess
import json
import sys
import traceback
dbfile="/home/william/Repos/YTPlayer/db.json"

def bashpipe(*args):
	procs=[]
	if len(args) > 1:
		procs.append(subprocess.Popen(args[0], stdout=subprocess.PIPE))
		for i in range(1, len(args)):
			procs.append(subprocess.Popen(args[i], stdin=procs[i-1].stdout, stdout=subprocess.PIPE))
		return procs[i].stdout.read()[:-1].decode("ascii")
	else:
		return ""

class YTPlayer:
	def __init__(self, dbfile):
		db = json.load(open(dbfile,"r"))
		while True:
			try:
				link = self.getnext(db)
				print("Next Link:", link)
				db["playlist"].append(link)
				del db["suggestions"][link]
				suggestions = self.getsuggestions(link)
				db = self.savesuggestions(db, link, suggestions)
				json.dump(db, open(dbfile, "w"))
				self.playsong(link)
			except KeyboardInterrupt:
				sys.exit(1)
			except:
				traceback.print_exc()
	
	def getnext(self, db):
		maxprec = 0
		nextlink = ""
		for link in db["suggestions"]:
			vote=0
			for prec in db["suggestions"][link]:
				vote=vote+int(db["suggestions"][link][prec])
			if vote > maxprec:
				maxprec = vote
				nextlink = link
		return link
		
	def playsong(self, link):
		subprocess.Popen(["mpv",link,"--no-video"], stdout=subprocess.PIPE).stdout.read()
		
	def savesuggestions(self, db, link, suggestions):
		for sugg in suggestions:
			if sugg not in db["playlist"]:
				if not hasattr(db["suggestions"], sugg):
					db["suggestions"][sugg] = {}
				db["suggestions"][sugg][link] = 4
		return db
		
	def getsuggestions(self, link):
		return bashpipe(["lynx","-dump",link],
						["grep","https://www.youtube.com/watch?v="],
						["tr","-s"," "],
						["cut","-d ","-f3"],
						["sort","-u"]).split("\n")

if __name__=="__main__":
	try:
		dbfile = sys.argv[1]
	except:
		pass
	YTPlayer(dbfile)

