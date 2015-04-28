#!/usr/bin/env python
# -*- coding: UTF-8 -*

from Stage import *



class TokenizerAdapter(Stage):

	""" Adaptador de interface para  etapas de tokenizadores utilizados"""


	def __init__(self,adapted,src_field='text',dst_field='text'):
		super(TokenizerAdapter,self).__init__(src_field,dst_field)
		self.adapted=adapted

	def setOutData(self,data):
		return ' '.join(data)

	def getData(self,data):
		return self.adapted.tokenize(data)
	

class TaggerAdapter(Stage):

	""" Adaptador de interface para etapas de taggers: sean de Chunks o Post"""

	def __init__(self,adapted,src_field='text',dst_field='tagged'):
		super(TaggerAdapter,self).__init__(src_field,dst_field)
		self.adapted=adapted
		

	def setOutData(self,data):
		return data

	def getData(self,data):
		

		try:
			return self.adapted.tag(data)
		
		except Exception,e:
			pass
		return None

class PersistenceAdapter(Stage):

	""" Adaptador de interface por si utiliza alguna etapa de persistencia de datos"""

	def __init__(self,adapted,src_field='chunked',dst_field='chunked'):
		
		super(PersistenceAdapter,self).__init__(src_field,dst_field)
		self.adapted=adapted

	def setOutData(self,data):
		return data

	def getData(self,data):
		self.adapted.add_and_save(data)
		return data

