#!/usr/bin/env python
# -*- coding: UTF-8 -*

from Tagger import *
from nltk.chunk import RegexpParser
from nltk.chunk.util import *
from nltk.util import *
from nltk.corpus import *
from TreeUtils import *
import json
import pickle
import pdb
import abc

class Chunker(Tagger):

	"""
		Tagger que opera sobre N-gramas ( chunks )
		El resultado es un texto etiquetado con las frases encontradas ( word post chunk)
	"""

	__metaclass__ = abc.ABCMeta

	
	def __init__(self,setupData):
		
		super(Chunker,self).__init__()
		self.fixer_function=None

	@abc.abstractmethod
	def tag(self,data):
		NotImplementedError("Subclass must implement this method")


class RegexpChunker(Chunker):
	
	"""
		Este tagger de n-gramas o chunker utiliza gramaticas para detectar frases.
		setupData: es el string de las gramaticas
		
	"""

	
	def __init__(self,setupData):
		super(RegexpChunker,self).__init__(setupData)
		self.chunker=RegexpParser(setupData)


	def tag(self,data): 

	  	if self.fixer_function:
	  		data=self.fixer_function(data)
		iobs=None
		try:
			parsedTree=self.chunker.parse(data)
			print parsedTree
			iobs= tree2conlltags(parsedTree)
		
		except Exception,e:
			pass
		return iobs	

		

class ModelChunker(Chunker):

	"""
		Este chunker utiliza un modelo probabilistico entrenado para detectar las frases.
		setupData: es el path del modelo a utlilizar.

	"""

	__metaclass__ = abc.ABCMeta

	def __init__(self,setupData):	
		
		super(ModelChunker,self).__init__(setupData)
		file_tagger_model=open(setupData,mode="rb")
		self.chunker=pickle.load(file_tagger_model)
		file_tagger_model.close()
		
		
	def tag(self,data):
		return self.toTuple(self.chunker.tag(data))
		
	def toTuple(self,data):
		
		"""
			Acomodar el formato de salida para que concuerde con el de RegexpChunker de modo que puedan intercambiarse sin dificultad.

		"""
		sent=[]
		for n_upla in data:
			word_post,iob=n_upla
			word,post=word_post
			sent.append((word,post,iob))
		return sent


