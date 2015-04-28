#!/usr/bin/env python
# -*- coding: UTF-8 -*

import nltk.chunk
from nltk.tag import ClassifierBasedTagger
from nltk.classify import *
from nltk.tag import *
import nltk.chunk, itertools
from nltk.corpus import conll2000
from nltk.corpus.reader import ConllChunkCorpusReader
import random
from nltk.corpus import names
from nltk.chunk import RegexpParser
import pdb
from nltk.chunk.util import *
from time import sleep
import os.path
from os import listdir
import pickle






class Classifier(nltk.TaggerI):

	"""
		Esta clase es mas bien un "ayudante" del sistema para generar el clasificador chunker de Bayes ingenuo.
		La extraccion de caracteristicas efectiva es un proceso de tipo prueba-error; por ende se implementa como una Strategy separado.
		Sus parametros de configuracion se encuentran en el archivo ./config/taggers.ini
		

	"""

	def __init__(self,train_sents,chunkers_path,extension_file,feature_extractor):
		
		self.chunkers_path=chunkers_path
		self.extension_file=extension_file
		self.feature_extractor=feature_extractor

		train_set=[]
		for sent in train_sents:
			
			history=[]
			untagged_sent=nltk.tag.untag(sent)
			for i, (word, tag) in enumerate(sent):
				features=feature_extractor.get_features(untagged_sent,i,history)
				if features:
					train_set.append((features,tag)) 
					history.append(tag)
					

			
		self.classifier=nltk.NaiveBayesClassifier.train(train_set)
		
		
	
	def save(self,chunker_name):
		if self.classifier:
			if not chunker_name:
				chunker_name=self.getDefaultName()
			f = open(chunker_name,'wb')
			pickle.dump(self, f)
			f.close()
		print ("Guardando el chunker :" + chunker_name)
		return chunker_name

	def getDefaultName(self):

		fname=self.chunkers_path+"chunker"
		fname=fname+str(len(listdir(self.chunkers_path)))+self.extension_file
		return fname
		
	def tag(self,sentence):

		history=[]
		for i,word in enumerate(sentence):
			features=self.feature_extractor.get_features(sentence,i,history)
			tag=self.classifier.classify(features)
			history.append(tag)
		tagged=zip(sentence,history)
		return tagged


class Chunker(nltk.ChunkParserI):

	def __init__(self,train_sents,chunkers_path,extension_file,feature_extractor):
		
	
		tagged_sents=[]
		for sent in train_sents:
			tagged_sent=[]
			for word,post,chunk in sent:
				tagged_sent.append(((word,post),chunk))
			tagged_sents.append(tagged_sent)	
		
		self.tagger=Classifier(tagged_sents,chunkers_path,extension_file,feature_extractor)

	def save(self,chunker_name=None):
		return self.tagger.save(chunker_name)

	def parse(self,sentence):
		tagged_sent=self.tagger.tag(sentence)
		conlltags = [(w,t,c) for ((w,t),c) in tagged_sent]
		return nltk.chunk.conlltags2tree(conlltags)


class ChunkerModelGenerator(object):


	
	def __init__(self,chunkers_path,corpus_path,files,phrases,training_portion,file_extension,feature_extractor):

		
		conllreader = ConllChunkCorpusReader(corpus_path,files,phrases)
		corpus=conllreader.iob_sents()
		
		size=float(len(corpus)*training_portion)
		size=int(size)

		train_sents=corpus[:size]
		test_sents=corpus[size:]

		self.tt=[]
		for  ts in test_sents:
			self.tt.append(conlltags2tree(ts))

		print "Porcentaje del corpus de entrenamiento:",training_portion
		print "Porcentaje del corpus para testing:",1-training_portion

		
		self.chunker=Chunker(train_sents,chunkers_path,file_extension,feature_extractor)

	
	def createModel(self):
				
		print self.chunker.evaluate(self.tt)
		return self.chunker.save()


