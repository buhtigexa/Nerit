#!/usr/bin/env python
# -*- coding: UTF-8 -*
import abc
class StageFactory(object):

	"""
		Interface a resperar por las Fabricas de objetos del pipe

	"""
	
	__metaclass__=abc.ABCMeta

	def __init__(self):
		pass

	def createInstance(self):
		pass

	def toStage(self,src_field,dst_field):
		"""	
			Adaptar las instancias.
			src_field y dst_field indican que campos de datos se operaran dentro del pipeline
			
		"""
		pass	