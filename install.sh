#!/bin/bash

apt-get install python-pip
pip install tweepy
wget https://bootstrap.pypa.io/ez_setup.py -O - | python
pip install -U nltk
pip install termcolor
pip install inflection

