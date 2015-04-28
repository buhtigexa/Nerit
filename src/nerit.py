#!/usr/bin/env python
# -*- coding: UTF-8 -*

from datasource.TwitterConnection import *
from datasource.FileConnection import *
from datasource.DataLineConnection import *
from NeritFacade import *
from Printer import *
import codecs
import pickle
import os
import sys
from filters.Filter import StringFilter
import os.path
from time import sleep

from grammars_fix import * #aqui tengo las gramaticas para corregir falsos negativos de las direcciones

"""
	Este modulo es la instanciacion del framework. 

"""

def usage():
	print " "
	print "[Opción] [argumentos]"
	print "-cpt 	Crear post tagger según archivo de configuración"
	print "-cct     Crear chunk tagger seǵun archivo de configuración"
	print "argumentos:    ruta del archivo de configuración para los taggers."
	print "-tc 		Procesar desde Twitter"
	print "argumentos: lista de hashtags. Ej 'tránsito, choque' "
	print "-lc 		Procesar desde archivo"
	print " "



def strToList(string_data):

	data_list=[]
	if isinstance(string_data,str):
		data_list=string_data.split()
	return data_list	


def createTwitterConnection(nerit,hashtags=[]):

	
	timeLine=True
	if hashtags:
		timeLine=False
	connection=nerit.getTwitterConnection(hashtags,timeLine)
	return connection


def getAdHocDecorator(grammar_location=locations,grammar_clean=clean):

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


def createPostStage(nerit,post_model):

	decoratorTagger=None#nerit.getDecoratorTagger()
	posTaggerStage=nerit.getTaggerStage(model_path=post_model,decorator=decoratorTagger)
	if os.path.exists(post_model):
		posTaggerStage=nerit.getTaggerStage(post_model,'text','tagged',decoratorTagger)

	return posTaggerStage
	

def createChunkStage(nerit,chunk_model):

	# combinar extracciones por metodo probabilistico y strategy de gramaticas para corregir los falsos negativos.

	decorator=nerit.getChunkerDecorator()
	chunkerStage=nerit.getChunkerStage(decorator=decorator) # hasta aqui, sólo va a utilizar puramente gramaticas para extraer direcciones y 
	# le aniadimos un poco mas de gramaticas para regifinar los sintagmas que buscamos. Recordar, que asi como esta primero va a usar la
	# gramatica "chunks"
	
	if os.path.exists(chunk_model):
		# pero si hay un modelo entrenado, lo utilizamos.
		
		decorator=getAdHocDecorator() # y también corregimos algunos errores con una estrategias de ayuda.( o podria utilizar las mismas que x regexp comentamos....)
		chunkerStage=nerit.getChunkerModelStage(model_path=chunk_model,decorator=decorator)
		print "\nUtilizando el modelo entrenado para extraer chunks:",chunk_model
		sleep(1.0)
	return chunkerStage



def createChunkStage_(nerit,chunk_model):

	# este es el que combina todo y no va a estar incluido en la solucion, porque combinar puramente expresiones ( que detectan direcciones desde
	# chunks básicos ( sintagmas nominales,verbales,etc) rompe la solucion anterior para luego aplicar una estrategia y refinar los sintagmas
	# normales en busca de direcciones y eventos. 
	
	chunkerStage=None
	if os.path.exists(chunk_model):
		chunkerStage=nerit.getChunkerWrappedStage(model_path=chunk_model,strategy=nerit.getChunkerStrategy())
		print "\nUtilizando el modelo entrenado para extraer chunks:",chunk_model
		sleep(1.0)

	return chunkerStage




def createPipeline(nerit,connection,tokenizers,abbreviations,post_model,chunk_model,save_to,strFilter,corpus_size,final_stage=None):

	# crear el pipeline con todas las etapas...
	
	try:
		tokenizerStage=nerit.getTokenizerStage(tokenizers,abbreviations)
		posTaggerStage=createPostStage(nerit,post_model)
		
		chunkerStage=createChunkStage(nerit,chunk_model)
		persistenceStage=nerit.getPersistenceStage(StringFilter(strFilter),save_to,corpus_size)
		
		nerit.add_finalStage(final_stage)
		
		pipeline=nerit.createPipeline([tokenizerStage,posTaggerStage,chunkerStage,persistenceStage])
		
		connection.addObserver(pipeline)
		connection.listen()

	except Exception,e:
		#print str(e)
		#pdb.set_trace()	
		pass


# configuracion estandar de la aplicacion .

config = ConfigParser.RawConfigParser()
config.optionxform = str 			
config.read("/home/marce/code/virtual_envs/nerit/config/nerit.ini")

nerit=NeritFacade()
connection=None

corpus_lf=config.get('test_file','test_1') # cada linea es solo texto del tweet
corpus_cf=config.get('test_file','test_2') # cada dato es un Json

tokenizers_file=config.get('tokenizers','tokenizers_file')
abbreviations=config.get('tokenizers','abbreviations') # un archivo de expresiones regulares para abreviaturas 
taggers_config=config.get('taggers','taggers_config') # la configuracion para los taggers
post_model=config.get('taggers','post_model') # que modelos utilizar 
chunk_model=config.get('taggers','chunk_model')
save_to=config.get('persistence','save_to') # si armo corpus, doonde lo dejo
corpus_size=config.getint('persistence','corpus_size')
strFilter=config.get('persistence','strFilter') # filtrar los datos que entraran al corpus que voy a generar 
phrases_to_print=phrases=[chunk_tag for ph_id,chunk_tag in config.items('noun_phrases')] # que frases quiero mostrar en pantalla

try:
	option=sys.argv[1]
	
	if option=='--h':
		usage()
			
	if option=='-cpt':
		# crear POS Tagger 
		if len(sys.argv)==3:
			taggers_config=sys.argv[2]
		nerit.createPosTagger(taggers_config)
		
	elif option=='-cct':
		# crear Chunk Tagger
		if len(sys.argv)==3:
			taggers_config=sys.argv[2]
		nerit.createChunkTagger(taggers_config)
		
	elif option=='-tc':
		# conectar a Tweeter para escuchar por tweets. Si no le paso hashtags, entonces lee desde el timeline 
		hashtags=[]
		if len(sys.argv)==3:
			hashtags=sys.argv[2]
			hashtags=strToList(hashtags)
		connection=createTwitterConnection(nerit,hashtags)

	elif option=='-lc':
		# conectate a un archivo de lineas de texto, cada linea es el texto de un tweet
		if len(sys.argv)==3:
			corpus_lf=sys.argv[2]
		connection=nerit.getDataLineConnection(corpus_lf)

	elif option=='-fc':
		# la considero una opcion menos requerida, pero mas bien para mostrar que el disenio permite multiples conexiones
		# conectar a un archivo de tweets ( completos, es decir en Json )
		if len(sys.argv)==3:
			corpus_cf=sys.argv[2]
		connection=nerit.getFileConnection(corpus_cf)
	

	if connection:
		# enchufar ultima etapa al pipeline 
		final_stage=Printer()
		# indicarle que frases quiero que imprima
		final_stage.set_target_chunks(phrases_to_print)
		createPipeline(nerit,connection,tokenizers_file,abbreviations,post_model,chunk_model,save_to,strFilter,corpus_size,final_stage)
		# salir andando...
		
except IndexError:
	usage()






