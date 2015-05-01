#!/usr/bin/env python
# -*- coding: UTF-8 -*


from datasource.TwitterConnection import *
from datasource.FileConnection import *
from datasource.DataLineConnection import *
from NeritFacade import *
import codecs
import pickle
import os
import sys
from filters.Filter import StringFilter
import os.path
from time import sleep
import abc
from grammars_fix import * #aqui tengo las gramaticas para corregir falsos negativos de las direcciones

"""
	Esta clases es el USO del FrameWork 

"""



class Menu(object):

	__metaclass__ = abc.ABCMeta

	def __init__(self,config_file):
		self.neritFacade=NeritFacade()
		self.config_file=config_file

	def strToList(self,string_data):

		data_list=[]
		if isinstance(string_data,str):
			data_list=string_data.split()
		return data_list	


	def createTwitterConnection(self,hashtags=[]):

		
		timeLine=True
		if hashtags:
			timeLine=False
		connection=self.neritFacade.getTwitterConnection(hashtags,timeLine)
		return connection


	def createPosTaggerModel(self,post_config_file):
		self.neritFacade.createPosTagger(post_config_file)

	def createChunkTaggerModel(self,post_config_file):
		self.neritFacade.createChunkTagger(post_config_file)

	def getJSONFileConnection(self,json_file_path):
		return self.neritFacade.getFileConnection(json_file_path)

	def createPostStage(self,post_model):

		decoratorTagger=None#nerit.getDecoratorTagger()
		posTaggerStage=self.neritFacade.getTaggerStage(model_path=post_model,decorator=decoratorTagger)
		if os.path.exists(post_model):
			posTaggerStage=self.neritFacade.getTaggerStage(post_model,'text','tagged',decoratorTagger)

		return posTaggerStage
		

	def createChunkStage(self,chunk_model):

		# combinar extracciones por metodo probabilistico y strategy de gramaticas para corregir los falsos negativos.

		decorator=self.neritFacade.getChunkerDecorator()
		chunkerStage=self.neritFacade.getChunkerStage(decorator=decorator) # hasta aqui, sólo va a utilizar puramente gramaticas para extraer direcciones y 
		# le aniadimos un poco mas de gramaticas para regifinar los sintagmas que buscamos. Recordar, que asi como esta primero va a usar la
		# gramatica "chunks"
		
		if os.path.exists(chunk_model):
			# pero si hay un modelo entrenado, lo utilizamos.
			
			decorator=self.getAdHocDecorator() # y también corregimos algunos errores con una estrategias de ayuda.( o podria utilizar las mismas que x regexp comentamos....)
			chunkerStage=self.neritFacade.getChunkerModelStage(model_path=chunk_model,decorator=decorator)
			print "\nUtilizando el modelo entrenado para extraer chunks:",chunk_model
			sleep(0.1)
		return chunkerStage


	def createPipeline(self,connection,tokenizers,abbreviations,post_model,chunk_model,save_to,strFilter,corpus_size,final_stage=None):

		# crear el pipeline con todas las etapas...
		
		try:
			tokenizerStage=self.neritFacade.getTokenizerStage(tokenizers,abbreviations)
			posTaggerStage=self.createPostStage(post_model)
			chunkerStage=self.createChunkStage(chunk_model)
			persistenceStage=self.neritFacade.getPersistenceStage(StringFilter(strFilter),save_to,corpus_size)
			self.neritFacade.add_finalStage(final_stage)
			pipeline=self.neritFacade.createPipeline([tokenizerStage,posTaggerStage,chunkerStage,persistenceStage])
			connection.addObserver(pipeline)
			connection.listen()

		except Exception,e:
			print str(e)
			pdb.set_trace()	
			

	def getDataLineConnection(self,line_file_path):
		
		return self.neritFacade.getDataLineConnection(line_file_path)


	def getAdHocDecorator(self,grammar_location=locations,grammar_clean=clean):

		# utilizar las gramáticas de grammars_fix.py para corregir falsos negativos.

		locations=PostPatternStrategy(grammar_location) # gramaticas para direcciones
		iobFixer=IOBFixerStrategy()						# """" iobFixer me permite acomodar el Arbol de Chunks luego de recortar por detectar frases.""""
		fixer=SequentialStrategy(locations,iobFixer)	# armar una estrategia para corregir direcciones usando la gramatica "locations"
		clean=PostPatternStrategy(grammar_clean)      # aplicar unos ajustes mas...
		fixer=SequentialStrategy(fixer,clean)
		fixer=SequentialStrategy(fixer,iobFixer)
		decorator=WrappedStrategyTagger()
		decorator.set_strategy(fixer)
		return decorator

	@abc.abstractmethod
	def getConfig(self):
		raise NotImplementedError("Subclass must implement this method")
	
	def usage(self):
	
		print " "
		print "[Opción] [argumentos]"
		print "-cpt 	Crear post tagger según archivo de configuración"
		print "-cct     Crear chunk tagger seǵun archivo de configuración"
		print "argumentos:    ruta del archivo de configuración para los taggers."
		print "-tc 		Procesar desde Twitter"
		print "argumentos: lista de hashtags. Ej 'tránsito, choque' "
		print "-lc 		Procesar desde archivo"
		print " "
	
	def show_menu(self,config):
		
		taggers_config=config.get('taggers','taggers_config')
		corpus_lf=config.get('test_file','test_1')
		corpus_cf=config.get('test_file','test_2')
		tokenizers_file=config.get('tokenizers','tokenizers_file')
		abbreviations=config.get('tokenizers','abbreviations')
		post_model=config.get('taggers','post_model')
		chunk_model=config.get('taggers','chunk_model')
		corpus_size=config.get('persistence','corpus_size') 
		strFilter=config.get('persistence','strFilter')
		save_to=config.get('persistence','save_to')
		phrases_to_print=[chunk_tag for ph_id,chunk_tag in config.items('noun_phrases')]

		try:
			connection=None
			option=sys.argv[1]
			if option=='--h':
				usage()
			if option=='-cpt':
				# crear POS Tagger 
				if len(sys.argv)==3:
					taggers_config=sys.argv[2]
				self.createPosTaggerModel(taggers_config)
			
			elif option=='-cct':
				# crear Chunk Tagger
				if len(sys.argv)==3:
					taggers_config=sys.argv[2]
				self.createChunkTaggerModel(taggers_config)
			
			elif option=='-tc':
				# conectar a Tweeter para escuchar por tweets. Si no le paso hashtags, entonces lee desde el timeline 
				hashtags=[]
				if len(sys.argv)==3:
					hashtags=sys.argv[2]
					hashtags=self.strToList(hashtags)
				connection=self.createTwitterConnection(hashtags)

			elif option=='-lc':
				# conectate a un archivo de lineas de texto, cada linea es el texto de un tweet
				if len(sys.argv)==3:
					corpus_lf=sys.argv[2]

				print "Corpus lf:",corpus_lf
				connection=self.getDataLineConnection(corpus_lf)

			elif option=='-fc':
				# la considero una opcion menos requerida, pero mas bien para mostrar que el disenio permite multiples conexiones
				# conectar a un archivo de tweets ( completos, es decir en Json )
				if len(sys.argv)==3:
					corpus_cf=sys.argv[2]
				connection=self.getJSONFileConnection(corpus_cf)
			else:
				usage()	

			if connection:
				self.final_stage.set_target_chunks(phrases_to_print)
				self.createPipeline(connection,tokenizers_file,abbreviations,post_model,chunk_model,save_to,strFilter,corpus_size,self.final_stage)
				# salir andando...
				
		except IndexError:
			self.usage()













