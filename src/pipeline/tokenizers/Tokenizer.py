#!/usr/bin/env python
# -*- coding: UTF-8 -*

import abc
import pdb
import logging
import json



class Tokenizer(object):

	"""
		Este tokenizar determina un marco de operacion general para todas las subclases.
		Todos los tokenizadores dividen las palabras por espacios y aplican transformaciones especificas.

	"""

	__metaclass__ = abc.ABCMeta

	def __init__(self,regexp,operation="",operation_state="True"):
		self.operation=operation
		self.operation_state=operation_state
		self.dict=json.load(open(regexp,"r"))
	
	def tokenize(self,data):


		tokens=[]
		splitted=data.split(" ") 
		try:
			for token in splitted:
				isCatch=False
				for key in self.dict.keys():
					if self.accept(key,self.operation,self.operation_state):
						isCatch,token,isMatch=self.onMatch(token,key,isCatch,tokens)
						if isMatch:
							break
		            
				if not isCatch:
					token=self.notMatch(token)
					if token:
						tokens.append(token)
	   
		except Exception,e:
			pass
			
		return tokens


	def notMatch(self,token):
		return token
      	
	@abc.abstractmethod	
	def onMatch(self,token,key,isCatch,tokens):
		"""
			Operacion a determinar al emparejar con un lexema
		"""
		raise NotImplementedError("Subclass must implement this method")

	def accept(self,key,operation,operation_state):

		"""
			Que hacer si el lexema adhiere ....
		"""
		return self.dict[key][operation]==operation_state
		

