#!/usr/bin/env python
# -*- coding: UTF-8 -*

from Source import Source
import codecs
import re
import pdb
import json


class FileConnection(Source):

	"""
  	Esta clase abre un archivo con datos en formato JSON y difunde los datos adquiridos en cada paso.

	""" 	
	
	def __init__(self,filePath,observers=[]):

		super(FileConnection,self).__init__(observers)

		self.tweet_token_separator='}}""'
		self.i=0
		try:
			self.fileInput=open(filePath)
		except IOError:
			print("File not found.Please provide a properly file path")
			exit(0)

	def on_data(self,data):

		try:
			self.notifyObservers(data)
		except KeyboardInterrupt:
			pdb.set_trace()
			
    
	def listen(self):
	
		accline=""
		for line in self.fileInput:
			accline=accline+line
			match=re.search(self.tweet_token_separator,line)
			if match:
				try:
					accline=accline[:-4]
					tweet=json.loads(accline)
					accline=""
					self.on_data(tweet)
				except KeyboardInterrupt:
					pdb.set_trace()
				except Exception,e:
					print str(e)
					pass
