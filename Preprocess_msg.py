

import numpy as np
import pandas as pd
import re
import nltk
# import spacy
import string
import csv

# !pip install emot
from emot.emo_unicode import UNICODE_EMO, EMOTICONS

#Importing stopwords from nltk library
from nltk.corpus import stopwords
nltk.download('stopwords')
STOPWORDS = set(stopwords.words('english'))

from textblob import TextBlob

from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
lemmatizer = WordNetLemmatizer()
wordnet_map = {"N":wordnet.NOUN, "V":wordnet.VERB, "J":wordnet.ADJ, "R":wordnet.ADV} # Pos tag, used Noun, Verb, Adjective and Adverb



def translator(user_string):
    user_string = user_string.split(" ")
    j = 0
    for _str in user_string:
        # File path which consists of Abbreviations.
        fileName = "slang_dict_edited_more.txt"
        # File Access mode [Read Mode]
        accessMode = "r"
        with open(fileName, accessMode) as myCSVfile:
            # Reading file as CSV with delimiter as "=", so that abbreviation are stored in row[0] and phrases in row[1]
            dataFromFile = csv.reader(myCSVfile, delimiter="`")
            # Removing Special Characters.
           # _str = re.sub('[^a-zA-Z0-9-_.]', '', _str)
            for row in dataFromFile:
                # Check if selected word matches short forms[LHS] in text file.
                if _str.upper() == row[0]:
                    # If match found replace it with its appropriate phrase in text file.
                    user_string[j] = row[1]
            myCSVfile.close()
        j = j + 1
    # Replacing commas with spaces for final output.
    return (' '.join(user_string))

def convert_emojis(text):
    for emot in UNICODE_EMO:
        text = text.replace(emot, "_".join(UNICODE_EMO[emot].replace(",","").replace(":","").split()))
    return text
def convert_emoticons(text):
    for emot in EMOTICONS:
        text = re.sub(u'('+emot+')', "_".join(EMOTICONS[emot].replace(",","").split()), text)
    return text
# Example
# text = "Hello :-) :-)"
# print(convert_emoticons(text))
# text1 = "Hilarious 😂"
# print(convert_emojis(text1))
# Passing both functions to 'text_rare'


def stopwords(text):
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])

def lemmatize_words(text):
    pos_tagged_text = nltk.pos_tag(text.split())
    return " ".join([lemmatizer.lemmatize(word, wordnet_map.get(pos[0], wordnet.NOUN)) for word, pos in pos_tagged_text])


#Creating function for tokenization
def tokenization(text):
    text = re.split('\W+', text)
    return text

def text_clean(text_file):
  filename=text_file
#   filename="asian_kreationz.txt"
  df=pd.read_csv(filename,header=None,error_bad_lines=False)
  print(df.head())
  df = df.iloc[1:]
  print(df.head())
  df["1"]=""
  df.columns=['Name', 'Chat']
  Message= df['Name'].str.split('\\):', n = 1, expand = True)
  print(Message.head())
  Message.columns=['Name_Time', 'Chat']
  Message1= Message['Name_Time'].str.split('\\(', n = 1, expand = True)
  print(Message1.head())
  result = pd.concat([Message1, Message], axis=1, sort=False)
  print(result.head())
  result= result.drop(['Name_Time'], axis = 1) 
  print(result.head())
  for i in result.index:
    x=re.search('[(](.*)[)]',str(result["Chat"][i]))
    if x is not None:
      result["Chat"][i] = result["Chat"][i].replace("("+str(x.group(1))+")","")
  # result.head() 
  result['Stage']=""
  result.to_csv(str(text_file)[:-4]+".csv")
  for i in range(1,len(result)) : 
    string= result.loc[i, 'Chat']
    if(string is None):
      continue
    result.loc[i, 'Chat']=translator(result.loc[i, 'Chat'])

  
  result['Chat'] = result['Chat'].fillna("").apply(convert_emoticons)
  result['Chat'] = result['Chat'].fillna("").apply(convert_emojis)
  #lowercasing
  result['text_lower']  = result['Chat'].str.lower()
  result['text_lower'].head()
  result.head()
  result['text_punct'] = result['text_lower'].str.replace('[^\w\s]','')
  result['text_punct'].head()
  result.head()
  result["text_stop"] = result["text_punct"].apply(stopwords)
  result["text_stop"].head()
  # print(result)
  
  if(string is None):
    result['text_stop'].apply(lambda x: str(TextBlob(x).correct()) if (len(x)!=0) else (x))

  result["text_lemma"] = result["text_stop"].apply(lemmatize_words)
  result['text_token'] = result['text_lemma'].apply(lambda x: tokenization(x.lower()))
  result[['text_token']].head()
  result.head(50)
  return result

filename="asian_kreationz.txt"
clean_dataset= text_clean(filename)
clean_dataset.to_csv("Preprocessed"+str(filename)[:-4]+".csv")




