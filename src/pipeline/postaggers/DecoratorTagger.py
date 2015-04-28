#!/usr/bin/env python
# -*- coding: UTF-8 -*

import abc 
from Tagger import *



class DecoratorTagger(Tagger):

	"""
		Envuelve un Tagger para que las subclases adicionen comportamiento.
		
	"""

	__metaclass__ = abc.ABCMeta

	def __init__(self,tagger=None):
		super(DecoratorTagger,self).__init__()
		self.tagger=tagger
		self.strategy=None

	

	def set_wrapped(self,wrapped_tagger):
		self.tagger=wrapped_tagger
