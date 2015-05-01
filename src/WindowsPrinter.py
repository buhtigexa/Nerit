#!/usr/bin/env python
# -*- coding: UTF-8 -*

from Printer import * 
import os

class WindowsPrinter(Printer):
	
	"""
		Clase bastante hardcodeada, pero es para una consola espefica.
		Muestra los resultados por pantalla adaptado a consola Windows.

	"""

	def __init__(self,target_chunks=[],to_show='LOCATION',sleep_time=4.0):
		super(WindowsPrinter,self).__init__(target_chunks,to_show,sleep_time)
		
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
	
	def pretty_print(self,feature,chunks):

		
		os.system("color 9")
		print "\n[TWEET ORIGINAL]"
		print feature['original'].encode('UTF-8')

		for key in self.chunks:
			os.system("color 9")
			print ('<<FRASES EXTRAIDAS>>')
			msg="<<Frase: "+key +" >>"
			print msg
			self.iprint(self.chunks[key],key)
			print " "

