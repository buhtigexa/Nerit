#!/usr/bin/env python
# -*- coding: UTF-8 -*

from StageFactory import *

from pipeline.postaggers.Chunker import *

from pipeline.Adapters import TaggerAdapter

class ChunkerFactory(StageFactory):

	""" 
		Fabrica abstracta de Chunkers
	"""

	def __init__(self,setupData=None):

		super(ChunkerFactory,self).__init__()
		self.setupData=setupData
		self.decorator=None
	
	

	def set_decorator(self,decorator):

		""" 
			Si se dispone de un wrapper, se utiliza 
		"""
		
		self.decorator=decorator
	
	def createInstance(self):

		"""
			Crear el tagger y wrappear si hay algun envoltorio

		"""

		chunker=self.getChunker(self.setupData) 
		if self.decorator:
			self.decorator.set_wrapped(chunker)
			chunker=self.decorator
	
		return chunker

	def toStage(self,src_field,dst_field):

		"""	
			Adaptar las instancias.
			src_field y dst_field indican que campos de datos se operaran dentro del pipeline
			
		"""

		tagger=self.createInstance()
		adapter=TaggerAdapter(tagger,src_field,dst_field)
		return adapter

	@abc.abstractmethod
	def getChunker(self,setupData):
		raise NotImplementedError("Subclass must implement this method")


class RegexpChunkerFactory(ChunkerFactory):

	""" 
		Fabrica de Taggers por gramaticas
	"""

	def __init__(self,setupData=None):
		"""
			setupData: que gramaticas utilizar
		"""
		super(RegexpChunkerFactory,self).__init__(setupData)

	def getChunker(self,setupData):
		return RegexpChunker(setupData)


class ModelChunkerFactory(ChunkerFactory):

	"""
		Fabrica de Taggers que utilizan modelos probabilisticos
	"""

	def __init__(self,setupData=None):
		""" setupData: que modelo utilizar
		"""
		super(ModelChunkerFactory,self).__init__(setupData)

	def getChunker(self,setupData):
		
		model= ModelChunker(setupData)
		return model