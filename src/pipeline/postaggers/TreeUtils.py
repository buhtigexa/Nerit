#!/usr/bin/env python
# -*- coding: UTF-8 -*
import re, itertools
import nltk.tag
from nltk.tree import Tree
import pdb
import re

""" Este modulo es un conjunto de utilidades para trabajar sobre los arboles de chunks
"""

def flatten_childtrees(trees):
	""" Se pude definir cualquier gramática recursiva. La gramática más simple va a dejar un arbol de 3 niveles (palabra-post-chunk). 
		Este método trata de llevar el arbol a 3 niveles, independiente de la profundidad de la gramatica.
	"""

	children = []
	try:
		for t in trees:
			if not isinstance(t,nltk.Tree):
				t=tuple2tree(t)
			elif t.height()==2:
				t=lowArbolToTree(t)
			if t.height() < 3:
				children.extend(t.pos())
			elif t.height() == 3:
				children.append(Tree(t.label(), t.pos()))
			else:
				children.extend(flatten_childtrees([c for c in t]))
	except Exception,e:
		pass
	return children

def flatten_deeptree(tree):

	return Tree(tree.label(), flatten_childtrees([c for c in tree]))

def tuple2tree(t):
	
	""" Convertir arboles a tuplas.
	"""
	word,tag=t
	tree=nltk.Tree(tag,[word])
	
	return tree

def lowArbolToTree(t):
	childs=[]
	treeTag=t.label()
	tree=None
	for n in t.leaves():
		if isinstance(n,tuple):
			childs.append(tuple2tree(n))
	tree=nltk.Tree(treeTag,childs)
	
	return tree


def ieertree2conlltags(tree, tag=nltk.tag.pos_tag):
   

    words, ents = zip(*tree.pos())
    iobs = []
    prev = None
    for ent in ents:
        if ent == tree.label():
            iobs.append('O')
            prev = None
        elif prev == ent:
            iobs.append('I-%s' % ent)
        else:
            iobs.append('B-%s' % ent)
            prev = ent
    words, tags = zip(*tag(words))
    return zip(words, tags, iobs)
			
def fixer_function(sentence):

	for i in range(0,len(sentence)-1):
  		prev_word,prev_pos=sentence[i-1]
  		curr_word,curr_pos=sentence[i]
  		next_word,next_pos=sentence[i+1]
  		if curr_pos=="IN" and "NN" in prev_pos and "NN" in next_pos:
			if curr_word=="de" or curr_word=="del":
  				sentence[i]=curr_word,"IN_DT"		
	return sentence

def map_tags(sentence,post=["IN"],tag=["INP"],words=['a','de','desde','hacia','bajo','sobre','tras','en','entre','hasta']):
	for i in range(0,len(sentence)):
		curr_word,curr_pos=sentence[i]
		if curr_word in words:
			sentence[i]=curr_word,tag[0]
	return sentence


def cleanIobs(words,post,locs,grammar_pattern_to_clean,modified_chunk_pattern,clean):
		
	new_tree=[]
	try:
		if len(words)!=len(locs):
			logging.info("[different list size]:")
			

		w,mid_iobs,out_iobs=zip(*locs)
		
		out_iobs=list(out_iobs)
		
		out_iobs=cleanSentence(out_iobs,grammar_pattern_to_clean,clean)

		mid_iobs=list(mid_iobs)

		mid_iobs=cleanSentence(mid_iobs,modified_chunk_pattern,clean)
		aux_iobs=zip(words,mid_iobs,out_iobs)
		aux_iobs=list(aux_iobs)
		out_iobs=[]
		for i in range(0,len(aux_iobs)):
			w,t,o=aux_iobs[i]
			if o=="O":
				out_iobs.append(t) 
			else:
				out_iobs.append(o)
		new_tree=zip(words,post,out_iobs)

	except Exception,e:
	
		pass

	return new_tree


def cleanSentence(list_tags,pattern_to_clean,pattern_replace):

	try:
		for i in range(0,len(list_tags)):
			list_tags[i]=re.sub(pattern_to_clean,pattern_replace,list_tags[i])

	except Exception,e:
		pass
		
	return list_tags	


def cleanIOB_Tag(iob):
	# Retorna el iob-tag sin la letra de inicio o inside ( sin B- o I-)
	
	word,tag,iob_tag=iob
	clean_iob=iob_tag.replace("B-","")
	clean_iob=clean_iob.replace("I-","")
	return word,tag,clean_iob
		

def isSameTag(iob_a,iob_b):
		
	# determina si dos tuplas tienen el mismo iob-tag
	w_a,t_a,c_a=cleanIOB_Tag(iob_a)
	w_b,t_b,c_b=cleanIOB_Tag(iob_b)
	if c_a==c_b:
		return True
	return False
		
def isTag(iob,tag):
		
	# determina si una tupla tiene un tag determinado
	w_a,t_a,c_a=cleanIOB_Tag(iob)
	if c_a==tag:
		return True
	return False

def tagIn(iob,tags_to_join):
	# determina si una tupla tiene algun tag del conjunto
	for iob_tag in tags_to_join:
		if isTag(iob,iob_tag):
			return True
	return False

def join_IOBS(chunked_sent,tags_to_join=['NOUNP','VERBP','ADVBP','PREPP']):

	# Une las frases que tienen el mismo tag ==> B-NP,I-NP,B-NP===> B-NP,I-NP,I-NP
	
	for i in range(0,len(chunked_sent)-1):
		word_curr,tag_curr,iob_curr=chunked_sent[i]
		word_next,tag_next,iob_next=chunked_sent[i+1]
		if "B-" in iob_next:
			if isSameTag(chunked_sent[i],chunked_sent[i+1]) and tagIn(chunked_sent[i],tags_to_join):
				word_next,tag_next,iob_next=cleanIOB_Tag(chunked_sent[i+1])
				chunked_sent[i+1]=word_next,tag_next,"I-"+iob_next
	return chunked_sent			


def fix_start_IOB(chunked_sent):
	
	# B-NP, I-NP, I-VP ===> B-NP,I-NP,B-VP
	# Si los tags de las chunks son distintos, y el proximo es distinto de O entonces, el siguiente añade una B. 

	for i in range(0,len(chunked_sent)-1):
		if not isSameTag(chunked_sent[i],chunked_sent[i+1]) and not isTag(chunked_sent[i+1],"O"):
			word,tag,iob_next=cleanIOB_Tag(chunked_sent[i+1])
			iob_next="B-"+iob_next
			chunked_sent[i+1]=word,tag,iob_next
	return chunked_sent


def fix_IOBS(chunked_sent,tags_to_fix=["O"]):

	# B-O, I-O ==> O, O 
	# si el tag está en el conjunto, sólo deja el tag limpio en la tupla
	
	for index in range(0,len(chunked_sent)):
		if tagIn(chunked_sent[index],tags_to_fix):
			chunked_sent[index]=cleanIOB_Tag(chunked_sent[index])
	return chunked_sent	

