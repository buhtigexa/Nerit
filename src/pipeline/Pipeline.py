#!/usr/bin/env python
# -*- coding: UTF-8 -*

import unicodedata
import re
import pdb 
import codecs
import json
from ObserverObservable import Observable,Observer
from termcolor import colored




class Pipeline(Observable,Observer):


	def __init__(self,observers=[]):
		
		super(Pipeline,self).__init__(observers)
		self.stages=[]
		self.corpus_list=[]

	def setLimit_process(self,limit_process):
		self.limit_process=limit_process


	def addStage(self,stage):
		self.stages.append(stage)

	
	def addFinalStage(self,stage):
		""" 
			Aniadir un observadores al final para operar sobre el salido del horno
		"""

		self.addObserver(stage)
	

	def update(self,data):
		self.execute(data)	

	def execute(self,feature):
		""" Ejecucion en secuencia, paso a paso dentro del Pipeline
		"""
		try:
			if not feature:
				
				return
			
			feature['original']=feature['text']
			for index in range(0,len(self.stages)):
				feature=self.stages[index].excecute(feature)
			# cuando lleges a la etapa final, emitir notificacion de que terminaste
			self.notifyObservers(feature)	

		except KeyboardInterrupt:
			# cortar el proceso sii te interrumpo forzosamente
			pdb.set_trace()		
			
		except Exception,e:
			# nunca frenes, siempre segui procesando

			pass

		return feature
