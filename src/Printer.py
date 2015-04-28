#!/usr/bin/env python
# -*- coding: UTF-8 -*

import abc
import pdb
import json
from ObserverObservable import Observer,Observable
from nltk.chunk.util import conlltags2tree,tree2conlltags
from time import sleep
from termcolor import colored
import re
from inflection import humanize
import codecs

class Printer(Observer):
	
	""" 
		Esta clase es la última etapa del pipeline. Muestra los resultados por pantalla.
	"""

	def __init__(self,target_chunks=[]):
		super(Printer,self).__init__()
		self.chunks={}
		self.target_chunks=target_chunks

		self.borrador=[]

	def set_target_chunks(self,target_chunks):
		self.target_chunks=target_chunks

	def update(self,data):
		
		
		self.chunks={}
		
		try:
			feature=data
			chunks=feature['chunked']
			tree=conlltags2tree(chunks)
			
			for chunk_name in self.target_chunks:
				succedded_chunk=self.getChunk(tree,chunk_name)
				if succedded_chunk:
					if chunk_name not in self.chunks:
						self.chunks[chunk_name]=succedded_chunk
			
			if "LOCATION" in str(self.chunks):
				print "-------------------------------------------------------------------------------------------------------------------------"
				
				print colored("\n[TWEET ORIGINAL]",'yellow')
				print feature['original'].encode('UTF-8')

				for key in self.chunks:
					print colored('[<<FRASES EXTRAÍDAS>>]:','blue')
					msg="<<Frase: "+key +" >>"
					print colored(msg,'green')
					self.iprint(self.chunks[key],key)
					print " "
				
				# frena un cachito para ver los resultados.

				sleep(4.0)
				
		except Exception,e:
			pass

	def iprint(self,msg,key):

		if key=="LOCATION":
			for data in msg:
				addr=humanize(data)
				addr=addr.decode('UTF-8')
				print "* ",addr
		else:		
			addr=' '.join(msg)
			print addr.decode('UTF-8')
			print " "

	def getChunk(self,tree,target_token):

		target=[]
		for subtree in tree.subtrees(filter=lambda t:target_token.lower() in t.label().lower()):
			word,post,iob_chunk=zip(*tree2conlltags(subtree))
			word=self.toString(word)
			target.append(word)
		

		return target

	def toString(self,tupla):

		string=""
		for word in tupla:
			string=string + " " + word.encode('UTF-8')
	
		return string


	

