#!/usr/bin/env python
# -*- coding: UTF-8 -*

import abc
import pdb
import codecs

from ObserverObservable import Observable

	
class Source(Observable):

	"""
		Interface a implementar por cualquier fuente de datos que deseemos procesar.
		
		*Nota-A MEJORAR*: para permitir un procesamiento mas fluido y romper la secuencialidad el metodo listen deberia hacer
		uso del patron PRODUCER-CONSUMER de modo que las fuentes puedan bloquearse y de ahi en mas el Pipeline 
		consumir lo que tiene hasta el momento, en lugar de depender todo el procesamiento desde los datos de entrada.

	"""

	__metaclass__=abc.ABCMeta

	def __init__(self,observers=[]):
		super(Source,self).__init__(observers)

	@abc.abstractmethod
	def listen(self):
		raise NotImplementedError("Subclass must implement this method")


	
	@abc.abstractmethod
	def on_data(self,data):
		raise NotImplementedError("Subclass must implement this method")


