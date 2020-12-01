# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 18:39:55 2020

@author: Randa Zarnoufi
"""

import gensim.models as gm
from nltk import edit_distance
import difflib
import time
import Soundex
import re
import pylcs
	 

# Function to remove vowels from a string
def removeVowels(str_input):
    ret = []
    str_out= ''
    vowels = 'o i e a u'
    first_letter=str_input[0]
    next_letters=str_input[1:]
    for char in next_letters:
        if char not in vowels:
            ret.append(char)
    str_out = first_letter + "".join(ret)
    return str_out

# Function to remove repeated characters more than twice in a string
def remove_repeat_char(word):
    regex = r"(.)\1{1,}"
    subst = "\\1"
    result = re.sub(regex, subst, word, 0, re.MULTILINE)
    return result

# Function to measure the lexical similarty between two strings
def lexsim(val1, val2):
    lcs = pylcs.lcs(val1, val2) # the longest common subsequence LCS
    lcsr = lcs/max(len(val1),len(val2)) # the longest common subsequence ratio LCSR
    lexsim = lcsr/edit_distance(val1,val2)
    return lexsim*100
  

# Function to extract the list of the different transliterations of the "canonicalWord" from the result (data) of the function most_similar (of gensim)
def getTheListOfTransliterations(data, canonicalWord):
    sim = 0.0
    norm_out=''
    finalArray = []
    for i in range(len(data)):
        transWord = data[i][0]
        if (canonicalWord.lower() == (transWord).lower()) or (transWord).isdigit():
            pass
        else:
            
            # replace 7 by h because in this stage they are both equivalent to [ḥ]
            val1 = re.sub('7', 'h', canonicalWord)
            val1 = remove_repeat_char(val1)

            val2 = re.sub('7', 'h', transWord)
            val2 = remove_repeat_char(val2)

            # MANorm lexical similarity measure
            if len(val1)>0 and len(val2)>0:
                seq = difflib.SequenceMatcher(None,removeVowels(val1),removeVowels(val2))                
                sim = seq.ratio()*100
                if sim >= 67.0 :
                    finalArray.append(transWord)  
            
            # SeqMatching
            # if len(canonicalWord)>0 and len(transWord)>0:
            #     seq = difflib.SequenceMatcher(None,canonicalWord,transWord)                
            #     sim = seq.ratio()*100
            #     if sim > 70.0 :
            #         finalArray.append(transWord)
            
            # Lexsim
            # sim = lexsim(canonicalWord,transWord)
            # if sim >= 70.0:
            #     finalArray.append(transWord)
            
            # Soundex
            # seq = difflib.SequenceMatcher(None,Soundex.soundex_ma(val1),Soundex.soundex_ma(val2))
            # sim = seq.ratio()*100
            # if sim > 70.0 :    
            #     finalArray.append(transWord)  

            else:
                pass
    return finalArray  


# Function for normalization dictionnary generation

def MaNorm_generation(document):
    string = ""
    listTransliterations = ''
    arrayTransliterations = []
    for mylines in document:
        canonicalWord = mylines.strip()

        try:
            listTransliterations = model.wv.most_similar(positive=[canonicalWord], topn=nbOfSimWords)
            arrayTransliterations = getTheListOfTransliterations(listTransliterations, canonicalWord)
        except:
            continue

        for l in arrayTransliterations:
            string = string + l + '\t' + canonicalWord + '\n'

    return string

# Create MANorm Dictionary 

filename = "MADic" # the dictionary of MA canonical words form.
nbOfSimWords = 20 # the number of the most similar words extracted 
document = open(filename+'.txt', 'r', encoding='utf8').readlines()

# get the word embedding models and generate normalization dictionaries
model = gm.Word2Vec.load('MA_Model/ma_model_Fastext')
resfile = open(filename + "_manorm_dictionary_fastext.txt", "w", encoding="utf-8")
resfile.write(MaNorm_generation(document))
resfile.close()

model = gm.Word2Vec.load('MA_Model/ma_model_skip_gram')
resfile = open(filename + "_manorm_dictionary_skipgram.txt", "w", encoding="utf-8")
resfile.write(MaNorm_generation(document))
resfile.close()

model = gm.Word2Vec.load('MA_Model/ma_model_cbow')
resfile = open(filename + "_manorm_dictionary_cbow.txt", "w", encoding="utf-8")
resfile.write(MaNorm_generation(document))
resfile.close()
