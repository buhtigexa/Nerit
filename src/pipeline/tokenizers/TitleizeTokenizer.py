#!/usr/bin/env python
# -*- coding: UTF-8 -*
import unicodedata
import re
import pdb 
import codecs
import json
import inflection
from Tokenizer import *



class TitleizeTokenizer(Tokenizer):

   """ 
      Reemplaza tokens por otra expresion regular. Ej: para hashtags o user mentions, puede eliminar el #/@ y aplicar CamelCase 
      para obtener las palabras que estan juntas.
       
   """

   def __init__(self,regexp,operation="titleize",regex="titleize_regex",replace="titleize_replace" ):

      super(TitleizeTokenizer,self).__init__(regexp,operation)
      self.regex=regex
      self.replace=replace  	

   
   def onMatch(self,token,key,isCatch,tokens):

      isMatch=False
      match=re.search(self.dict[key][self.regex],token,flags=re.IGNORECASE)
      if match:
         token=re.sub(self.dict[key][self.regex],self.dict[key][self.replace],token)
         if token:
            token=inflection.titleize(token)
            token=token.lower()
            isCatch=False
            isMatch=True
      return isCatch,token,isMatch

   	