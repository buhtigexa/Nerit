#!/usr/bin/env python
# -*- coding: UTF-8 -*

import abc



class Filter(object):
	
	__metaclass__ = abc.ABCMeta

	def __init__(self):
		pass

	@abc.abstractmethod
	def eval(self,data):
		raise NotImplementedError("Subclass must implement this method")

class TrueFilter(Filter):

	""" Es un filtro vacio, cualquiera sea el dato retorna True"""

	def __init__(self):
		super(TrueFilter,self).__init__()
	
	def eval(self,data):
		return True

class StringFilter(Filter):

	""" Filtro para conocer si un dato cualquiera ( pues se transforma a String) contiene determinada palabra"""
	
	def __init__(self,target):
		super(StringFilter,self).__init__()
		self.target=target
		
	def eval(self,data):
		if self.target in str(data):
			return True
		return False
		
