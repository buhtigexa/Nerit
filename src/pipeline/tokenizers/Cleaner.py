#!/usr/bin/env python
# -*- coding: UTF-8 -*
import unicodedata
import re
import pdb 
import codecs
import json
from Tokenizer import *
import string





class Cleaner(Tokenizer):
	"""
		Permie realizar el borrado de tokens que pertenecen a caracteres de escape o codificaciones que salen del vocabulario espaniol.
		
	"""

	def __init__(self,regexp="./Tokenizers.re",operation="clean",regex="regex"):
		super(Cleaner,self).__init__(regexp,operation)
		self.regex=regex

	def onMatch(self,token,key,isCatch,tokens):

		isMatch=False
		match=re.search(self.dict[key][self.regex],token,flags=re.IGNORECASE)
		if match:
			isCatch=True
			isMatch=True
		return isCatch,token,isMatch	

