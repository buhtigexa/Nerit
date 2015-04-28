#!/usr/bin/env python
# -*- coding: UTF-8 -*

import abc
import pdb


class Strategy(object):


	""" 
		
		Esta clase es la interface algortimo que actúa sobre una lista de triplas, es decir, sobre los chunks en formato de triplas.
		Toma como entrada una lista de triplas, y sale con otra lista de triplas.

	"""
	__metaclass__ = abc.ABCMeta

	def __init__(self):
		pass

	@abc.abstractmethod
	def fix(self,feature):
		raise NotImplementedError("Subclass must implement this method")


class IdempotentStrategy(Strategy):

	""" Estrategia que no modifica nada
	"""
	def __init__(self):
		pass

	def fix(self,feature):
		return feature


class SequentialStrategy(Strategy):

	""" Aplica 2 estrategias en secuencia
	"""
	def __init__(self,wrapped_strategy_first,wrapped_strategy_next):
		super(SequentialStrategy,self).__init__()
		self.wrapped_strategy_first=wrapped_strategy_first
		self.wrapped_strategy_next=wrapped_strategy_next

	def fix(self,feature):
		feature=self.wrapped_strategy_first.fix(feature)
		return self.wrapped_strategy_next.fix(feature)


