#!/usr/bin/env python
# -*- coding: UTF-8 -*


import re
import sys
import os
import pdb
from nltk.corpus import conll2002
from nltk.corpus.reader import ConllChunkCorpusReader,WordListCorpusReader
import pickle
from nltk import UnigramTagger, BigramTagger, TrigramTagger,NgramTagger,RegexpTagger
from nltk.tag import NgramTagger
import os.path
from os import listdir
import ConfigParser
import json


 




class PostModelGenerator():

	"""
		"Ayudante" de la aplicacion para generar un modelo de Pos Tagging. 
		El modelo realiza un etiquetado por n-gramas; al momento de incertidumbre de clasificacion se apoya en un clasificador de (n-i)-gramas.
		Para las palabras que por su morfologia son facilmente etiquetadas se etiquetan via 1-gramas por expresiones regulares.
		Las palabras desconocidas se etiquetan como las mas frecuentes del corpus.
		Todos los parametros de configuracion se encuentran en /config/taggers.ini

	"""

	def __init__(self,config_file):
		
		try:
		
			self.config = ConfigParser.RawConfigParser()
			self.config.optionxform = str 			
			self.config.read(config_file)
			
			tokenizers=self.config.get('post_training_corpus','regex_file')
			self.config_tokenizer=json.load(open(tokenizers,"r"))
			
			self.isWordList=self.config.getboolean('postaggers','isWordList')	
			self.wordlist=self.config.items('postaggers.wordlist')
			self.training_portion=self.config.getfloat('post_training_corpus','training_portion')
			self.taggers_path=self.config.get('postaggers','save_to')
			self.max_ngrams=self.config.getint('postaggers','max_ngrams')
			self.tagger_extension_file=self.config.get('postaggers','ext_file')
			corpus=[]

			for key,corpus_file in self.config.items('post_training_corpus.corpus'):
				print "Generate model from file:",corpus_file
				corpus.append(corpus_file)
	
			self.corpusReader=ConllChunkCorpusReader(self.config.get('post_training_corpus','corpora'),corpus,('NP','PP','VP','AP'))
			self.corpusSents=self.corpusReader.tagged_sents()
		
			self.wordListReader=WordListCorpusReader(self.config.get('post_training_corpus','wordlist_path'),r'.*\.txt')
			
			self.regex_list=[]
		
			
			for key in self.config_tokenizer.keys():
			
				if self.config_tokenizer[key]['isolate']=="True":
					regex=self.config_tokenizer[key]['regex'].encode('utf-8').decode('utf-8')
					post=self.config_tokenizer[key]['post']
					self.regex_list.append((regex,post))
					
			
			#logging.info(self.regex_list)
		
		except Exception,e:
			
			print "Error :", str(e)
			pdb.set_trace()
			
	def buildUnigrams(self):
	
		try:
			unigrams=[]
			wlist=None
			if self.isWordList:
				for post,list_file_name in self.wordlist:
					unigrams.append(self.getWordList(list_file_name,post))

		except Exception,e:
			#logging.error("Error",exc_info=True)
			#logging.debug( "this= %r", wlist)
			#logging.info("[build unigrams]Error: " + str(e))
			pass
			
		return unigrams	     	

	def getWordList(self,list_name,tag):
		
	
		wordlist=[]
		wlist=self.wordListReader.words(list_name)	
		for word in wlist:
			if not word or not tag:
				pdb.set_trace()
			wordlist.append((word,tag))
		return wordlist

	def createModel(self):

		
		model_name=None
		try:
			unigrams=self.buildUnigrams()
			
			N=len(self.corpusSents)
			toTraining=round(self.training_portion*N)
			
			#logging.info("Sentencias totales:" + str(N))

			training=self.corpusSents[:toTraining]
			test=self.corpusSents[toTraining:]
			
			post_patterns=[]

			for regex,post in self.regex_list:
				try:
					regex=regex.decode('utf-8')
				except:
					pass
				
				post_patterns.append((regex,post))


			
			for regex,post in self.config.items('postaggers.regex'):
				post_patterns.append((regex.decode('utf-8'),post))

		
			regexpTagger  = RegexpTagger(post_patterns)
			unigramTagger = UnigramTagger(unigrams+training,backoff=regexpTagger)	
			bigramTagger= BigramTagger(training, backoff=unigramTagger) 
			trigramTagger = TrigramTagger(training, backoff=bigramTagger)
			NTagger=NgramTagger(self.max_ngrams,training,backoff=trigramTagger)

			print("Sentencias de entrenamiento para n-taggers:" + str(len(training)))
			print("Sentencias de entrenamiento para unitaggers:" + str(len(unigrams)))
			print("Cantidad de palabras ADICIONALES de DICCIONARIOS para el unitagger:" + str(len(unigrams)))
			print("Sentencias para testing:" + str(len(test)))
			print("Expresiones regulares para el Tagger:")
			
			for post_regex in post_patterns:
				print post_regex
				
		
			if self.training_portion!=1:
		
				score_ut=unigramTagger.evaluate(test)
				score_bt=bigramTagger.evaluate(test)-0.002
				score_tt=trigramTagger.evaluate(test)
				score_nt=NTagger.evaluate(test)

			

				scores=[score_ut,score_bt,score_tt,score_nt]
				tagger_names=["uTagger","biTagger","triTagger","NTagger"]
				taggers=[unigramTagger,bigramTagger,trigramTagger,NTagger]

				bestTagger_index= scores.index(max(scores))
				best_msg=max(scores),tagger_names[bestTagger_index]
			
		
			fname=self.taggers_path + tagger_names[bestTagger_index]
			if os.path.isfile(fname+self.tagger_extension_file):
				fname=fname+str(len(listdir(self.taggers_path)))+self.tagger_extension_file
			else:
				fname=self.taggers_path + tagger_names[bestTagger_index]+self.tagger_extension_file
			
			model=taggers[bestTagger_index]

			f = open(fname,'wb')
			pickle.dump(model, f)
			f.close()
			
			print ("Guardando el tagger :" + fname)
			#logging.info("Guardando el mejor tagger :" + fname)
			
			model_name=fname
			
		except Exception,e:
			print "ERRPR EN POS TAGGER GENERATOR:",str(e)
			pdb.set_trace()
			
		return model_name


