#!/usr/bin/env python
# -*- coding: UTF-8 -*

from DecoratorTagger import *
from Tagger import *
import pdb



class WrappedStrategyTagger(DecoratorTagger):

	"""
		Wrapper que permite aniadir responsabilidad a la salida del etiquetador envuelto.

	"""

	def __init__(self,tagger=None):
		super(WrappedStrategyTagger,self).__init__(tagger)
		
	def set_strategy(self,strategy):
		"""
			He aqui la estrategia para enriquecer comportamiento.

		"""
		self.strategy=strategy

	def tag(self,data):

		sentence=self.tagger.tag(data)
		sentence=self.strategy.fix(sentence)
		return sentence


