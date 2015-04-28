#!/usr/bin/env python
# -*- coding: UTF-8 -*

from StageFactory import *
from pipeline.tokenizers.IsolateTokenizer import *
from pipeline.tokenizers.Cleaner import *
from pipeline.tokenizers.AbbrExpander import *
from pipeline.tokenizers.TitleizeTokenizer import *
from pipeline.Adapters import TokenizerAdapter

class TokenizerFactory(StageFactory):

	"""
		Encapsula la creacion de Tokenizadores y puede retornar las instancias con interface acorde para enchufar en el Pipe"


	"""


	def __init__(self,tokenizer_file,abbrs_file):
		super(TokenizerFactory,self).__init__()
		self.tokenizer_file=tokenizer_file
		self.abbrs=abbrs_file


	def addRegex(self,tokenizer,regexp):
		pass

	def createInstance(self):

		isolateTokenizer=IsolateTokenizer(self.tokenizer_file)
		cleanerTokenizer=Cleaner(self.tokenizer_file)
		abbrExpander=AbbrExpander(self.abbrs)
		titleizeTokenizer=TitleizeTokenizer(self.tokenizer_file)	

		return isolateTokenizer,cleanerTokenizer,abbrExpander,titleizeTokenizer,abbrExpander

	def toStage(self,src_field,dst_field):

		"""	
			Adaptar las instancias.
			src_field y dst_field indican que campos de datos se operaran dentro del pipeline
			
		"""
		tokenizers=self.createInstance()
		staged=[]
		
		for tokenize in tokenizers:
			staged.append(TokenizerAdapter(tokenize,src_field,dst_field))
		
		return staged

