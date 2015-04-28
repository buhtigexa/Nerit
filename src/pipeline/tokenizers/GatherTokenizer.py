#!/usr/bin/env python
# -*- coding: UTF-8 -*

import unicodedata
import re
import pdb 
import codecs
import json
from Tokenizer_ import *
import string



class GatherTokenizer (Tokenizer):

	""" 
		Este tokenizador fue utilizado para pruebas y actualmente no lo incluyo en la solucion final.
		La idea es colectar tokens agrupados por su morfologia. Ej: puedo juntar bajo el key "hashtag" todos los hashtag; "link" todos las urls;etc.
		Estos tokens pueden o no seguir en el texto original a procesar. El objetivo final seria poder procesar texto limpio y tener acceso
		a los datos que no aparecen. Ej: tengo la direccion de un evento y aparte del texto, saber quien lo posteo o las imagenes que lo acompanian.

	"""

	def __init__(self,regexp_path="./gatherTokenizer_regexp.re",src_field='text',dst_field='text',operation="gather",regex="regex",separate='separate'):
		
		"""
			regexp_path: el archivo donde defino expresiones regulares para tokens particulares ( darles tratamiento especial )
			field: el campo del json sobre el cual operar.
		"""

   		super(GatherTokenizer,self).__init__(src_field,dst_field,operation)
   		self.dict=json.load(open(regexp_path,"r"))
   		self.separate=separate
  
   		self.regex=regex
   		self.post="post"

   

	def addtoken(self,token_class,token,token_dict):

		""" Este metodo separa los tokens en otro campo. Agrupa los tokens en categorias, pues utiliza un hashtable"""

		if token_class not in token_dict:
					
			token_dict[token_class]=[]
			token_dict[token_class].append(token)
		else:
			token_dict[token_class].append(token)

	def onMatch(self,token,key,isCatch,tokens):
		
		isMatch=False
		match=re.search(self.dict[key][self.regex],token)
		if match:
			self.addtoken(self.dict[key][self.post],token,isolate_tokens)
			isCatch=False
			isMatch=True
		return isCatch,token,isMatch



