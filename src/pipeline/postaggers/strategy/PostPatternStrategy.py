#!/usr/bin/env python
# -*- coding: UTF-8 -*

from __future__ import division
from nltk.chunk import ChunkParserI
from nltk.chunk.util import conlltags2tree,tree2conlltags
import nltk.tag
from nltk.chunk import ChunkParserI
import re
import pdb
from Strategy import *
from ..TreeUtils import *
from nltk.chunk import RegexpParser
import codecs

from time import sleep

from termcolor import colored




class PostPatternStrategy(Strategy):

	"""
		Hay casos en que las frases que deseamos detectar se basan en las palabras mas que en su clase gramatical. Tambien podemos 
		ser mas precisos si podemos considerar distintos niveles del arbol, por ejemplo frases y palabras juntas dentro de una regla como un unico token.
		Esta estrategia permite mirar el arbol en altura y ancho, de modo que las gramaticas que escribamos podran ser mas presicas y flexibles.


	"""
	
	def __init__(self,grammar="",loop=2):
		super(PostPatternStrategy,self).__init__()		
		self.postChunker=RegexpParser(grammar,loop)
		self.grammar=grammar
		self.loop=loop

	def fix(self, feature):
		
		cleanSentence=feature
		tree=None
		try:
			
			grammar_pattern_to_clean=r'_.*' # caracter de separacion de niveles dentro de un mismo token.
			clean_pattern=''
			modified_chunk_pattern=r'.*_'
			words,post,iobs=zip(*feature)
			wiobs=tuple(w+"_"+iob for w,iob in zip(words,iobs)) # las sentencias a parsear ahora no consideran el POS TAG, sino IOBS y palabras.
			sentence=zip(words,wiobs)
			tree=self.postChunker.parse(sentence)
		  	loc_tags=tree2conlltags(flatten_deeptree(tree)) # voy de arbol a lista de tuplas de nuevo.
			cleanSentence=cleanIobs(words,post,loc_tags,grammar_pattern_to_clean,modified_chunk_pattern,clean_pattern)
	  		

		except Exception,e:
			pass

	  	return cleanSentence



	
	

	
	