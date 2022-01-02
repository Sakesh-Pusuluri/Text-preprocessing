import numpy as np
import pandas as pd
import re
import nltk
import spacy
import string
nltk.download('stopwords') # download stopwords from nltk library
from nltk.corpus import stopwords
from string import digits
from bs4 import BeautifulSoup
from nltk.stem.porter import PorterStemmer
from spellchecker import SpellChecker
class TextPreprocess():
  ''' With this class, we can do lower casing, removal of punctuations, removal of stopwords,  removal of digits, removal of html tags, 
      removal of emoji's, removal of url's, stemming, spelling correction'''
  def __init__(self):
      pass
  def clean_raw_text(self,text,remove_html=False,lower_case = False,remove_punctuation = False,remove_stopwords=False,remove_digits=False,remove_emoji=False,remove_urls=False,stemming=False,spell_correction=False):
    '''
    text --> Text data that to be cleaned,
    if remove_html is True, it will remove the html tags and then return the text
    if lower_case is True, it will convert the text to lower case
    if remove_punctuation is True, will remove the punctuations (!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
    if remove_stopwords is True,it will remove all the stopwords in our text
    if remove_digits  is True, it will remove all the digits in our text
    if remove_emoji is True, it will remove the emoji's in our text
    if remove_urls is True, it will remove the urls in our text
    if stemming is True , then it will do stemming
    if spell_correction is True, then it will correct our spellings 
    '''
    if remove_html:
      text =BeautifulSoup(text, "lxml").text
    if lower_case:
      text = str(text).lower()
    if remove_punctuation:
      text=text.translate(str.maketrans('','',string.punctuation))
    if remove_stopwords:
      stop_words= set(stopwords.words('english'))
      text = (' '.join([word for word in str(text).split() if word not in stop_words]))
    if remove_digits:
      text=text.translate(str.maketrans('','',digits))
    if remove_emoji:
      # https://stackoverflow.com/a/49146722/330558
      emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
      text = emoji_pattern.sub(r'', text)
    if remove_urls:
      url_pattern = re.compile(r'https?://\S+|www\.\S+')
      text = url_pattern.sub(r'', text)
    if stemming:
      stemmer = PorterStemmer()
      text = (' '.join([stemmer.stem(word) for word in str(text).split()]))
    if spell_correction:
      # https://norvig.com/spell-correct.html
      spell = SpellChecker()
      corrected_text = []
      misspelled_words = spell.unknown(text.split())
      for word in text.split():
          if word in misspelled_words:
              corrected_text.append(spell.correction(word))
          else:
              corrected_text.append(word)
      text = " ".join(corrected_text) 
    return text
