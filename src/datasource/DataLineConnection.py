#!/usr/bin/env python
# -*- coding: UTF-8 -*

from Source import Source
import codecs
import pdb		

class DataLineConnection(Source):
	
	"""
	
	Esta conexion permite leer desde una archivo de texto, y por cada linea emitir su aviso. 
	Esta clase seria mas bien una conexion de ejemplo
	"""

	def __init__(self,filePath,observers=[]):
		super(DataLineConnection,self).__init__(observers)
		self.iFile=codecs.open(filePath,encoding="UTF-8")
		
	def on_data(self,data):
		self.notifyObservers(data)
		
	def listen(self):
		
		""" Comenzar a "escuchar" el texto...
		"""


     	
		try:	
			for dataLine in self.iFile:
				if dataLine:
					feature={}
					feature['text']=dataLine
					self.on_data(feature)	
							

		except KeyboardInterrupt,e:
			pass
			
