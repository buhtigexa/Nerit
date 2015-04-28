#!/usr/bin/env python
# -*- coding: UTF-8 -*

import abc
import pdb
import json
import re
from ..Stage import *

class Tagger(object):

	__metaclass__ = abc.ABCMeta

	"""
		Interface a respetar por los etiquetadores que utilice la aplicacion.
		Las subclases deben subrogar el metodo tag.
		
	"""
	
	def __init__(self):
		pass

	@abc.abstractmethod	
	def tag(self,data):
		raise NotImplementedError("Subclass must implement this method")

	

	

	
	

