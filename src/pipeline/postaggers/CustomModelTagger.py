#!/usr/bin/env python
# -*- coding: UTF-8 -*

from Tagger import *
import pickle

class CustomModelTagger(Tagger):

	"""
		Eqituetador que utiliza modelos probabilisticos para realizar etiquetado de tokens.
		model: el path al modelo serializado a utilizar
	"""

	def __init__(self,model):
		super(CustomModelTagger,self).__init__()
		file_tagger_model=open(model,mode="rb")
		self.tagger=pickle.load(file_tagger_model)
		file_tagger_model.close()
	
	def tag(self,data):

		tagged_sent=self.tagger.tag(data.lower().split(" "))
		return tagged_sent

