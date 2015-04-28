#!/usr/bin/env python
# -*- coding: UTF-8 -*
import unicodedata
import re
import pdb 
import codecs
import json


from Tokenizer import *
	
class AbbrExpander(Tokenizer):
	
	""" Toma los tokens y compara contra expresiones regulares que corresponden a abreviaturas conocidas
		Cuando el token adhiere a dicha expresion regular se reemplaza por la aplicacion de la misma
	""" 

	def __init__(self,regexp,operation=""):
   		super(AbbrExpander,self).__init__(regexp,operation)

   		

   	
	def onMatch(self,token,key,isCatch,tokens):
		isMatch=False
		match=re.search(key,token,flags=re.IGNORECASE)
		if match:
			correct=re.sub(key,self.dict[key],token,flags=re.IGNORECASE)
			tokens.append(correct)
			isCatch=True
			isMatch=True
		return isCatch,token,isMatch

	def accept(self,key,operation,operation_state):
		return True