# Word Embedding
import nltk
import sys


# load corpus file
# file1 = open("MA_Normalization/corpus_out.txt",'r', encoding="utf8")
# text1 = file1.read()
# file1.close()

# file2 = open("MA_Normalization/corpus_out_4.txt", "r", encoding='utf8')
# text2 = file2.read()
# file2.close()
# text = text1 + text2

file = open("MA_Normalization/corpus_out3.txt",'r', encoding="utf8")
text = file.read()
file.close()


# preprocessing: sentence splitting, tokenization, lower case
sentences_out=[]
sentences = [p for p in text.split('\n') if p]
#print(sentences[:2])
for sentence in sentences:
    words = sentence.lower().split()
    sentences_out.append(words)


# import word2vec 
from gensim.models import Word2Vec

# train model (skip-gram sg=1/ CBOW sg=0)
w2v_cbow_model = Word2Vec(sentences_out, min_count=2, sg=0, hs=1, window=7, size=300, iter=10)
# train model (skip-gram sg=1/ CBOW sg=0)
w2v_skipg_model = Word2Vec(sentences_out, min_count=2, sg=1, hs=1, window=7, size=300, iter=10)

# save model
w2v_skipg_model.save('MA_Normalization/ma_model_skip_gram_03')
w2v_cbow_model.save('MA_Normalization/ma_model_cbow_04')

# With FASTEXT
from gensim.models import FastText
fastext_model = FastText(size=100, window=7, min_count=2, sentences=sentences_out, iter=10)
# save model
fastext_model.save('MA_Normalization/ma_model_Fastext_03')


# summarize the loaded model
print(w2v_skipg_model)
print(w2v_cbow_model)

# summarize vocabulary
words = list(w2v_cbow_model.wv.vocab)
#print(words)


