#!/usr/bin/python3

import sys
import traceback
import json
dbfile="/home/william/Repos/YTPlayer/db.json"

if __name__ == "__main__":
	try:
		dbfile = sys.argv[2]
	except:
		pass
	try:
		cmd = sys.argv[1]
		if cmd == "up":
			db = json.load(open(dbfile, "r"))
			playing = db["playlist"][-1]
			for song in db["suggestions"]:
				for prec in db["suggestions"][song]:
					if prec == playing:
						db["suggestions"][song][prec] = db["suggestions"][song][prec]*2
			json.dump(db, open(dbfile, "w"))
		elif cmd == "down":
			db = json.load(open(dbfile, "r"))
			playing = db["playlist"][-1]
			for song in db["suggestions"]:
				for prec in db["suggestions"][song]:
					if prec == playing:
						db["suggestions"][song][prec] = db["suggestions"][song][prec]/2
			json.dump(db, open(dbfile, "w"))
		elif cmd == "remove":
			db = json.load(open(dbfile, "r"))
			playing = db["playlist"][-1]
			for song in db["suggestions"]:
				deletions=[]
				for prec in db["suggestions"][song]:
					if prec == playing:
						deletions.append(prec)
				for deletion in deletions:
					del db["suggestions"][song][deletion]
			json.dump(db, open(dbfile, "w"))
	except:
		traceback.print_exc()
