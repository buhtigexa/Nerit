#!/usr/bin/env python
# -*- coding: UTF-8 -*

import pdb
from Strategy import *
from ..TreeUtils import *
from time import sleep

class IOBFixerStrategy(Strategy):

	"""
		La deteccion de frases deja como resultado un arbol cuyos nodos se etiquetan con palabras, post y frases.
		Cuando detectamos y re etiquetamos frases el arbol dejara inconsistentes algunos tags. Ej: si dentro 
		de una frase sustantiva reconocemos un evento, necesitamos reacomodar los tags. Ej: B-SUSTANTIVO I-SUSTANTIVO I-EVENTO
		debe quedar como B-SUSTANTIVO I-SUSTANTIVO B-EVENTO.
		Esta clase realiza dichas correcciones, entre otras, para dejar el arbol en estados consistentes ante suscesivas modificaciones.

	"""

	def __init__(self,grammar=""):
		super(IOBFixerStrategy,self).__init__()

	def fix(self,feature):
		
		
		try:
		
			feature=fix_IOBS(feature)

			# B-NP, I-NP, I-VP ===> B-NP,I-NP,B-VP
			# Si los tags de las chunks son distintos, y el proximo es distinto de O entonces, el siguiente añade una B. 

			feature=fix_start_IOB(feature)

			# Une las frases que tienen el mismo tag para formar frases mas largas ==> B-NP,I-NP,B-NP===> B-NP,I-NP,I-NP

			feature=join_IOBS(feature)

				
		except Exception,e:
			
			pass


		return feature