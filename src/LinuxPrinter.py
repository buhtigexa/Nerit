#!/usr/bin/env python
# -*- coding: UTF-8 -*

from Printer import *
from termcolor import colored

class LinuxPrinter(Printer):

	"""
		Clase bastante hardcodeada, pero es para una consola espefica.
		Muestra los resultados por pantalla adaptado a consola Linux
	"""

	
	def __init__(self,target_chunks=[],to_show='LOCATION',sleep_time=4.0):
		super(LinuxPrinter,self).__init__(target_chunks,to_show,sleep_time)	
	
	def pretty_print(self,feature,chunks):
	
		
				
		print colored("\n[TWEET ORIGINAL]",'yellow')
		print feature['original'].encode('UTF-8')
		for key in chunks:
			
			print colored('[<<FRASES EXTRAIDAS>>]:','blue')
			msg="<<Frase: "+key +" >>"
			print colored(msg,'green')
			self.iprint(chunks[key],key)
			print " "		

	def iprint(self,msg,key):
	
		if key==self.to_show:
			for data in msg:
				addr=humanize(data)
				addr=addr.decode('UTF-8')
				print "* ",addr
		else:		
			addr=' '.join(msg)
			print addr.decode('UTF-8')
			print " "