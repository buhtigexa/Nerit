#!/usr/bin/env python
# -*- coding: UTF-8 -*

from StageFactory import StageFactory

from pipeline.postaggers.CustomModelTagger import CustomModelTagger
from pipeline.Adapters import TaggerAdapter
import pdb

class TaggerFactory(StageFactory):

	"""
		Encapsula la creacion de Taggers y puede retornar las instancias con interface acorde para enchufar en el Pipe". Todo en un mismo conjunto


	"""

	def __init__(self,model_tagger,fix_strategy=None):
		
		super(TaggerFactory,self).__init__()
		self.model_tagger=model_tagger
		self.fix_strategy=fix_strategy
		self.decorator=None
		
	
		
	def set_model_tagger(self,model_tagger):
		self.model_tagger=model_tagger 

	def set_decorator(self,decorator):
		
		self.decorator=decorator
	
	def createInstance(self):
		"""
			Crear el tagger y wrappear si hay algun envoltorio

		"""

		tagger=None
		try:
			tagger=CustomModelTagger(self.model_tagger)
			if self.decorator:
				self.decorator.set_wrapped(tagger)
				tagger=self.decorator


		except Exception,e:
			pass
			
		return tagger

	def toStage(self,src_field,dst_field):

		"""	
			Adaptar las instancias utilizando el Adaptador correspondientes
			src_field y dst_field indican que campos de datos se operaran dentro del pipeline
			
		"""
		adapter=None
		try:
			tagger=self.createInstance()
			adapter= TaggerAdapter(tagger,src_field,dst_field)

		except Exception,e:
			pass

		return adapter

