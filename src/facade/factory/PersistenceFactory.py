#!/usr/bin/env python
# -*- coding: UTF-8 -*



from StageFactory import *
from pipeline.persistence.Store import *
from pipeline.Adapters import PersistenceAdapter

class PersistenceFactory(StageFactory):

	"""
		Fabrica de objetos de persistencia. Util para el caso de desear crear un corpus 
	"""

	def __init__(self,corpora_path,file_extension,corpus_size,iFilter):
		
		super(PersistenceFactory,self).__init__()
		self.corpora_path=corpora_path
		self.file_extension=file_extension
		self.corpus_size=corpus_size
		self.filter=iFilter

		
	
	def set_corpus_size(self,corpus_size):
		self.corpus_size=corpus_size


	def createInstance(self): 

		return Store(self.corpora_path,self.file_extension,self.corpus_size,self.filter)

	def toStage(self,src_field,dst_field): 

		"""	
			Adaptar las instancias.
			src_field y dst_field indican que campos de datos se operaran dentro del pipeline
			
		"""

		tagger=self.createInstance()
		adapter=PersistenceAdapter(tagger,src_field,dst_field)
		return adapter
