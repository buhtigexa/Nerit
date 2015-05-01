#!/usr/bin/env python
# -*- coding: UTF-8 -*
import ConfigParser
from Menu import Menu
from WindowsPrinter import WindowsPrinter
class NeritWin(Menu):

	""" Clase cliente ejecutable para Windows"""


	def __init__(self,config_file='..\\config\\nerit_win.ini'):
		super(NeritWin,self).__init__(config_file)

	def getConfig(self):
		
		config = ConfigParser.RawConfigParser()
		config.optionxform = str 
		self.final_stage=WindowsPrinter()
		config.read(self.config_file)
		return config

menu=NeritWin()
config=menu.getConfig()
menu.show_menu(config)
