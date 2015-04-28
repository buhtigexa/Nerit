#!/usr/bin/env python
# -*- coding: UTF-8 -*

import abc
import pdb



class Stage(object):
	
	""" Encapsula una de las etapas en el Pipeline"""

	__metaclass__ = abc.ABCMeta

	def __init__(self,src_field='text',dst_field='text'):
		self.src_field=src_field
		self.dst_field=dst_field
		
		
	def excecute(self,feature):

		""" 
			Feature es una hashtable que tiene los datos a procesar.
			En este método simplemente se toman datos desde un campo, se procesarán ( por una subclase) y se guardan en el campo indicado
			No se descartan campos anterires.
			

		"""
		
		data=feature[self.src_field]
		data_list=[]
		try:
			
			data_list=self.getData(data)

		except Exception,e:
			pass

			
		feature[self.dst_field]=self.setOutData(data_list)
		return feature


	@abc.abstractmethod
	def setOutData(self,data):
		raise NotImplementedError("Subclass must implement this method")
	
	@abc.abstractmethod
	def getData(self,data):
		raise NotImplementedError("Subclass must implement this method")
		