#!/usr/bin/env python
# -*- coding: UTF-8 -*

import abc
import os.path
from os import listdir
import codecs
import pdb
from time import sleep
from filters.Filter import StringFilter,TrueFilter

from Persistence import Persistence

class Store(Persistence):

	"""
		Esta clase guarda la salida del pipeline como un corpus en un archivo.
		No es necesario indicar el nombre del archivo pues se numera en forma incremental.
		La aplicacion no deberia requerir por parte del usuario esta operatoria, pues entonces 
		se utiliza como un medio para ayuda al testing de los clasificadores que pueda generar.
		Nota: se puede generar tanto un corpus de salida de POST con tuplas (word post) o bien salida de etiquetado de frases( word port chunk)

	"""

	def __init__(self,corpora_path,file_extension,corpus_size,iFilter):
		
		self.corpora_path=corpora_path
		self.file_extension=file_extension
		self.corpus_size=corpus_size
		self.corpus_list=[]
		self.isSave=False
		self.filter=iFilter
	
	
	
	def set_filter(self,iFilter):
		self.filter=iFilter

	def set_size(self,size):
		self.corpus_size=size

	
	def add_and_save(self,data):

		
		self.add(data)
		

		if self.isSave==False:
			if self.corpus_size>=1:
				if len(self.corpus_list) >= self.corpus_size:
					self.save()
				
		

	def save(self):
		try:
			
			if self.corpus_list:
				filename=str(self.corpora_path)+str(len(listdir(self.corpora_path)))+self.file_extension
				f=codecs.open(filename,"w",encoding="UTF-8")
				
				for sent in self.corpus_list:
					self.writeSent(sent,f)
				f.close()
				
				self.corpus_list=[]
				self.isSave=True
		
		except Exception,e:
			pass
			
	def clear(self):
		
		self.corpus_list=[]
		self.isSave=False

	

	def writeSent(self,sent,out_file):
		for tupla in sent:
			self.writeLine(tupla,out_file)
		out_file.write("\n")

	def writeLine(self,tupla,out_file):

		try:
			word=pos=iob=""
			
			if len(tupla)==2:
				word,pos=tupla
				line=word+" "+pos+"\n"

			elif len(tupla)==3:
				word,pos,iob=tupla
				line=word+" "+pos+" "+" "+iob+"\n"
			
			if word and pos:
				out_file.write(line)
		except Exception,e:
			pass
			
	def add(self,data):

		if self.filter.eval(data) and self.corpus_size>0:
			self.corpus_list.append(data)
