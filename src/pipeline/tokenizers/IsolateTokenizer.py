#!/usr/bin/env python
# -*- coding: UTF-8 -*

import unicodedata
import re
import pdb 
import codecs
import json
from Tokenizer import *
import string





class IsolateTokenizer (Tokenizer):

	"""
		Filtra/Aisla tokens de interes para evitar su desmenuzamiento y puede reemplazarlos por otro formato(borrado de espacios). 
		Ej: urls,fechas,temperaturas,horas,etc.
		Los tokens que bypassean el filtro son separados de signos de puntuacion redundantes. Ej: "correr;" ==> "correr"


	"""

	def __init__(self,regexp,operation="isolate",regex="regex",extra_operation="dirty_words",extra_replace="replace"):
		

   		super(IsolateTokenizer,self).__init__(regexp,operation)
		self.regex=regex
   		self.extra_operation=extra_operation
   		self.extra_replace=extra_replace

   	
   	def isolateCommon(self,token):
   		


		isolateToken=re.sub(self.dict[self.extra_operation][self.regex],self.dict[self.extra_operation][self.extra_replace],token)		
		return isolateToken



	def onMatch(self,token,key,isCatch,tokens):
		
	
		isMatch=False
		
		match=re.search(self.dict[key][self.regex],token,flags=re.IGNORECASE)
		if match:
			tokens.append(match.group())
			isCatch=True
			isMatch=True
		return isCatch,token,isMatch

	def notMatch(self,token):
		return self.isolateCommon(token)