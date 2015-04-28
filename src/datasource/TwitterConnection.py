#!/usr/bin/env python
# -*- coding: UTF-8 -*

from Source import Source
import tweepy
import json
import pdb




class TwitterConnection(Source,tweepy.StreamListener):

    # Cambiar los argumentos para decirle si quiere escuchar por hashtags o por el timeline
    
    def __init__(self,observers=[],access_token="2884744426-ZuFvaw0XC0qLw9AtkuPA7pK2sDSXgHKgnU7de9B"
                ,access_token_secret="Fcu5v7MXhKvIL2TPGQfSL4RZVnGe9yRqrWER9Zn61SUjX"
                ,consumer_key="dxci3lACHisj7NLpteCY6WSms"
                ,consumer_secret="2F6CXGvqCpsYOMXWQjvEgOJz2iiYPCCzot8po2fuqwLAaMAu6g"
                ,hashtags=[],timeLine=True,tweet_fields=['text']):


     
      super(TwitterConnection,self).__init__(observers)
      

      """

      Si no se indican "hashtags", se escucha el timeLine ( los usuarios seguidos )

      tweet_fields: son los campos que se consideran del tweet. No importa si se escucha desde el timeLine o de un stream de hashtags

      """
     
      auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
      auth.set_access_token(access_token, access_token_secret)
      api = tweepy.API(auth)
      self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
      self.auth.set_access_token(access_token, access_token_secret)
      self.stream = tweepy.Stream(auth, self)

      self.timeLine=timeLine
      self.tweet_fields=tweet_fields
      self.hashtags=hashtags
     
      if self.hashtags:
        self.timeline=False
        print " Hashtags:",self.hashtags
        



    def on_data(self, data):

      """
        Cada vez que se recibe un tweet se toman los campos que se indicaron, se encapsulan en una hashtable, y se difunden a los Observers

      """

      feature={}
      try:
        isIn=False
        status=json.loads(data)
        for key in self.tweet_fields:
          if key in status:
            isIn=True
            feature[key]=status.get(key) 
        
        if isIn:
          self.notifyObservers(feature)    
      
      except KeyboardInterrupt:
        pdb.set_trace()
      except KeyError:
        pass    
      
      


     

    def listen(self):
    
      """
      Comenzar a escuchar, o bien desde el timeLine o bien desde el stream de hashtags ( es exclusivo )

     """

      if self.timeLine:    
        self.stream.userstream()
      elif self.hashtags:
        self.stream.filter(track=self.hashtags)
    
    def on_error(self, status):
        pass
























