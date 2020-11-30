# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 19:30:16 2019

@author: Randa Zarnoufi
"""
# MA Soundex


import re

def soundex_ma(word):
    # Uppercase the first letter
    first_letter = word[0].upper()
    word_convert = word[1:]
    # Remove vowels
    word_convert = re.sub(r'[aeiouAEIOU]', '', word_convert)
    # Characters conversion
    outstring = ""
    for i in range (0, len(word_convert)):
        nextletter = word_convert[i]
        if nextletter in ['b','f', 'm', 'p','v', 'w']:
            outstring = outstring + '1'

        elif nextletter in ['d','t', 'l', 'n']:
            outstring = outstring + '2'

        elif nextletter in ['s','z']:
            outstring = outstring + '3'

        elif nextletter in ['j', 'y']:
            outstring = outstring + '4'

        elif nextletter in ['r']:
            outstring = outstring + '5'

        elif nextletter in ['9', 'q']:
            outstring = outstring + '6'
       
        elif nextletter in ['3', '7', 'h' , 'e']:
            outstring = outstring + '7'
        
        elif nextletter=='c':
            if word_convert[i+1] =='h':
                outstring = outstring + '4'
            else:
                outstring = outstring + '5'
                
        elif nextletter in ['k', 'g']:
            if word_convert[i+1]=='h':
                outstring = outstring + '5'
            else:
                outstring = outstring + '5'
            
    word_convert = first_letter + outstring
        
    return word_convert   
    
