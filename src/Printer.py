#!/usr/bin/env python
# -*- coding: UTF-8 -*

import abc
from ObserverObservable import Observer,Observable
from nltk.chunk.util import conlltags2tree,tree2conlltags
from time import sleep
from inflection import humanize

class Printer(Observer):

	__metaclass__ = abc.ABCMeta
	
	""" 
		Esta clase es la última etapa del pipeline. Muestra los resultados por pantalla
	"""

	def __init__(self,target_chunks,to_show,sleep_time):
		super(Printer,self).__init__()
		self.chunks={}
		self.target_chunks=target_chunks
		self.to_show=to_show
		self.sleep_time=sleep_time
		

	def set_target_chunks(self,target_chunks):
		self.target_chunks=target_chunks

	def update(self,data):

		self.chunks={}
		try:
			feature=data
			chunks=feature['chunked']
			tree=conlltags2tree(chunks)
			
			for chunk_type in self.target_chunks:
				succedded_chunk=self.getChunk(tree,chunk_type)
				if succedded_chunk:
					if chunk_type not in self.chunks:
						self.chunks[chunk_type]=succedded_chunk			
			
			if self.to_show in str(self.chunks):
				print "-------------------------------------------------------------------------------------------------------------------------"
				self.pretty_print(feature,self.chunks)
				sleep(self.sleep_time)
				
		except Exception,e:
			print str(e)
			pass

	
	@abc.abstractmethod
	def iprint(self,msg,key):
		raise NotImplementedError("Subclass must implement this method")

	@abc.abstractmethod
	def pretty_print(self,feature,chunks):
		raise NotImplementedError("Subclass must implement this method")

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
	




	


	

