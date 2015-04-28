#!/usr/bin/env python
# -*- coding: UTF-8 -*

import abc
import pdb

class Observable(object):

	

	__metaclass__ = abc.ABCMeta

	def __init__(self,observers=[]):
		self.observers=observers


	def addObserver(self,observer):
		
		
		self.observers.append(observer)
		

	def notifyObservers(self,data):
		for o in self.observers:
			o.update(data)


class Observer(object):

	__metaclass__ = abc.ABCMeta


	def __init__(self):
		pass

	@abc.abstractmethod
	def update(self,data):
		raise NotImplementedError("Subclass must implement this method")
