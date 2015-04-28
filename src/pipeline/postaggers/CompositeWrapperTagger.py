#!/usr/bin/env python
# -*- coding: UTF-8 -*

from Tagger import *
import pdb
 


class CompositeWrapperTagger(Tagger):

	"""
		Aplica Taggers en secuencia, canalizando la salida de uno como entrada del siguiente. 
		La idea es poder aniadir funcionalidad dinamicamente.

	"""

	def __init__(self,first_tagger=None,sec_tagger=None):
		super(CompositeWrapperTagger,self).__init__()
		self.first_tagger=first_tagger
		self.sec_tagger=sec_tagger


	def tag(self,data):

		sentence=self.first_tagger.tag(data)
		sentence=self.sec_tagger.tag(sentence)
		return sentence




