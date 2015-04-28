#!/usr/bin/env python
# -*- coding: UTF-8 -*


from datasource.FileConnection import FileConnection
from datasource.TwitterConnection import TwitterConnection
from datasource.DataLineConnection import DataLineConnection
from pipeline.postaggers.generators.ChunkerModelGenerator import ChunkerModelGenerator
from pipeline.postaggers.generators.PosTaggerModelGenerator import *
from pipeline.postaggers.WrappedStrategyTagger import WrappedStrategyTagger
from pipeline.postaggers.CompositeWrapperTagger import CompositeWrapperTagger
from pipeline.postaggers.strategy.Strategy import SequentialStrategy
from pipeline.postaggers.strategy.PostPatternStrategy import PostPatternStrategy
from pipeline.postaggers.strategy.IOBFixerStrategy import IOBFixerStrategy
from pipeline.Pipeline import Pipeline

from facade.factory.TokenizerFactory import TokenizerFactory
from facade.factory.ChunkerFactory import ChunkerFactory,RegexpChunkerFactory,ModelChunkerFactory
from facade.factory.PersistenceFactory import PersistenceFactory
from facade.factory.TaggerFactory import TaggerFactory
from pipeline.Adapters import TaggerAdapter

from grammars import *


from pipeline.postaggers.generators.features.FeatureExtractor import ContextFeatureExtractor


class NeritFacade(object):



	
	def __init__(self):
		
		self.pipeline=Pipeline()



	def createPosTagger(self,config_file):

		# crear un Tagger para POS usando PostModelGenerator como ayudante

		postModelGenerator=PostModelGenerator(config_file)
		model=postModelGenerator.createModel()
		return model

	def createChunkTagger(self,config_file):

		# crear un Tagger entrenado segun los parametros de /config/taggers.ini utilizando  ChunkerModelGenerator como clase "ayudante"
		


		config = ConfigParser.RawConfigParser()
		config.optionxform = str 			
		config.read(config_file)
		
		phrases=[ph for tag,ph in config.items('chunkers.phrases')]
		files=[fname for key,fname in config.items('chunk_training_corpus.corpus')]
		featureName=config.get('chunker.features','featureExtractor')
		chunkerGenerator=ChunkerModelGenerator(config.get('chunkers','save_to'),config.get('chunk_training_corpus','corpora'),files,phrases,config.getfloat('chunk_training_corpus','training_portion'),config.get('chunkers','ext_file'),ContextFeatureExtractor())

		model=chunkerGenerator.createModel()
		return model

	
	def getTokenizerStage(self,tokenizers_file,abbreviations,src_field='text',dst_field='text'):

		# crear etapa de Tokenizacion completa y adaptar para que enchufe en el Pipe

		tokenizerFactory=TokenizerFactory(tokenizers_file,abbreviations)
		tokenizerStages=tokenizerFactory.toStage(src_field,dst_field)
		return tokenizerStages


	def getTaggerStage(self,model_path,src_field='text',dst_field='tagged',decorator=None):

		# crear etapa de etiquetado gramatical y adaptar para que encaje en el Pipe

		factory=TaggerFactory(model_path)
		factory.set_decorator(decorator)
		stage=factory.toStage(src_field,dst_field)
		return stage

	
	def getChunkerModelStage(self,model_path,src_field='tagged',dst_field='chunked',decorator=None):

		# crear etapa de reconocimiento de Chunks basada en modelo entrenado.Adaptada al pipe.
		
		factory=ModelChunkerFactory(model_path)
		factory.set_decorator(decorator)
		
		stage=factory.toStage(src_field,dst_field)
		return stage	


	
	def getPersistenceStage(self,iFilter,save_to,corpus_size=-1,f_ext=".tcs",src_field='chunked',dst_field='chunked'):

		# Opcional: dejar como una etapa mas en el pipe por si se desea armar un corpus con la salida del pipe.

		factory=PersistenceFactory(save_to,f_ext,corpus_size,iFilter)
		stage=factory.toStage(src_field,dst_field)	
		return stage


	def createPipeline(self,stage_list):

		# armar el pipe con todas las etapas indicadas por stage_list

		for s in stage_list:
			if isinstance(s,list):
				for s_i in s:
					self.pipeline.addStage(s_i)
			else:
				self.pipeline.addStage(s)
				
		return self.pipeline


	def add_finalStage(self,stages):

		# determinar etapa final del pipe. Recordar que el Pipe es Observador, pero tambien Subject y puede emitir notificaciones al culminar su proceso.

		if isinstance(stages,list):
			for stage in stages:
				self.pipeline.addFinalStage(stage)
		else:
			self.pipeline.addFinalStage(stages)

	
	def pipe(self):
		return self.pipeline
	

	def getDataLineConnection(self,filename):

		# instancias una conexion para archvios linea-por-linea

		return DataLineConnection(filename)



	def getFileConnection(self,filename):

		# instanciar una conexion contra archivos con formato Json

		return FileConnection(filename)




	def getTwitterConnection(self,hashtags=[],timeLine=True):

		# contectarme a Twitter: puedo usar hashtags o procesar el timeline

		return TwitterConnection(hashtags=hashtags,timeLine=timeLine)

	
	def getChunkerStrategy(self,grammar_location=locations,grammar_events=events,grammar_words=words,grammar_clean=clean):

		# retorna puramente una estrategia. Es más bien una prueba....
	
		locations=PostPatternStrategy(grammar_location) #loop=3
		
		location_words=PostPatternStrategy(grammar_words)#loop=1
		locations=SequentialStrategy(locations,location_words)
				
		iobFixer=IOBFixerStrategy()
		locations_words_strategy=SequentialStrategy(locations,iobFixer)
		events=PostPatternStrategy(grammar_events) #loop=1
		events=SequentialStrategy(locations_words_strategy,events)
		events=SequentialStrategy(events,iobFixer)
		
		return events

	def getChunkerDecorator(self,grammar_location=locations,grammar_events=events,grammar_words=words,grammar_clean=clean):

		# un decortator ( que detecta sintagmas nominales,adverbiales,etc ) y se aniade funcionalidad para detectar direcciones y eventos 
		
	
		locations=PostPatternStrategy(grammar_location)
		
		location_words=PostPatternStrategy(grammar_words)
		locations=SequentialStrategy(locations,location_words)
		
		
		iobFixer=IOBFixerStrategy()
		locations_words_strategy=SequentialStrategy(locations,iobFixer)
		
		# busquemos por eventos dentro del arbol de chunks 
		events=PostPatternStrategy(grammar_events)
		events=SequentialStrategy(locations_words_strategy,events)

		events=SequentialStrategy(events,iobFixer)
		
		# decorador 
		decorator=WrappedStrategyTagger()
		decorator.set_strategy(events)
		
		return decorator


	def getChunkerStage(self,grammar_chunks=chunks,src_field='tagged',dst_field='chunked',decorator=None):	


		factory=RegexpChunkerFactory(grammar_chunks)
		factory.set_decorator(decorator)
		
		stage=factory.toStage(src_field,dst_field)

		return stage

	

	def getChunkerWrappedStage(self,model_path,grammar_chunks=chunks,src_field='tagged',dst_field='chunked',strategy=None):

		# Me va a servir para pruebas

		# armar un chunker para detectar frases utilizando corpus y luego las gramáticas ( desde cero: desde sintagmas nominales,preposicionales,etc )
		# arma un chunker combinando dos decorators y aplica en secuencia.


		factory=ModelChunkerFactory(model_path)
		modelChunker=factory.createInstance()
		
		factory=RegexpChunkerFactory(grammar_chunks)
		regexpChunker=factory.createInstance()
		
		wrappedRegexpChunker=WrappedStrategyTagger(regexpChunker)
		# estrategia para reconocer direcciones sobre los sintagmas estandar 
		wrappedRegexpChunker.set_strategy(strategy)	

		compositeTagger=CompositeWrapperTagger(modelChunker,wrappedRegexpChunker)
		chunkerStage=TaggerAdapter(compositeTagger,src_field,dst_field)

		return chunkerStage

 