#!/usr/bin/env python
# -*- coding: UTF-8 -*

import abc


class FeatureExtractor(object):
	__metaclass__ = abc.ABCMeta
	
	def __init__(self):
		pass

	@abc.abstractmethod	
	def get_features(self,tokens,index,history):
		raise NotImplementedError("Subclass must implement this method")



class ContextFeatureExtractor(FeatureExtractor):

	def __init__(self):
		pass


	


	def get_features(self,tokens,index,history):

		prevword,prevpos,previob=('<START>',)*3
		actual_word,actual_pos=tokens[index]
		nextword,nextpos,nextiob=('<END>',)*3

		word=actual_word
		pos=actual_pos

		feats={}
		
		if index>0:

			prev_word,prev_pos=tokens[index-1]
			prev_iob=history[index-1]

			prevpos=prev_pos
			previob=prev_iob
			prevword=prev_word

		if index < len(tokens)-1:

			next_word,next_pos=tokens[index+1]
			
			nextpos=next_pos
			nextword=next_word


		feats['prevword']=prevword
		feats['prevpos']=prevpos
		feats['previob']=previob
		feats['word']=word
		feats['pos']=pos
		feats['nextword']=nextword
		feats['nextpos']=nextpos
		feats['nextiob']=nextiob

		return feats

