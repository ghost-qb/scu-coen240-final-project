"""
Santa Clara University

COEN 240 - Machine Learning

Final Project

Quan Bach
Anh Truong



By running thi file: 
    - 2 plots will be produced and saved to Doc2vec folder 
    - these plots are doc2vec with distributed bags of words and doc2vec with distributed memory 
    
    
*** NOTICE ***: this script will dowload the 20 news group dataset from sklearn and perform processing directly here before the lda models. 
Therefore, it does not used the vocabularies generated by other files previously. However, the content should be the same. 


"""


import os
import gensim
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from sklearn.datasets import fetch_20newsgroups
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import pandas as pd 
from sklearn.manifold import TSNE
import numpy as np

# Tokenize and lemmatize

def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))
def preprocess(text):
    result=[]
    for token in gensim.utils.simple_preprocess(text) :
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
            
    return result


if __name__ == '__main__':
    
    if not os.path.exists('./Doc2Vec/'):
           os.makedirs('./Doc2Vec/')
    
    stemmer = SnowballStemmer("english")
    # load data 
    newsgroups_train = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes'), shuffle = True)    
    
    # initialize empty list to hold all docs 
    processed_docs = []
    
    # process the docs
    print('Loading dataset.....')
    for idx in range(0,len(newsgroups_train.data)):
        print(str(newsgroups_train.filenames[idx]))
        processed_docs.append(preprocess(newsgroups_train.data[idx]))
    
    print('Dataset loaded...')
    print('Set up and train Doc2Vec...')
    print('...')
    print('Training in progress')
    print('...')
    # convert processed docs into gensim formated tagged data 
    tagged_data = [TaggedDocument(doc,[i]) for i, doc in enumerate(processed_docs)]
   
    # train doc2vec model with dm = 0 i.e. training algorithm with distributed  bag of words 
    model_dbow = Doc2Vec(tagged_data, 
                   vector_size=89, 
                   window=2,
                   min_count=1,
                   workers=4,
                   epochs=100,
                   dm=0)
    # train doc2vec model with dm = 1 i.e. training algorithm with distributed memory 
    model_dm = Doc2Vec(tagged_data, 
                   vector_size=89, 
                   window=2,
                   min_count=1,
                   workers=4,
                   epochs=100,
                   dm=1)
   
    # save trained doc2vec model S
    model_dbow.save('./Doc2Vec/20newsgDoc2vec_DBOW_trained.model')
    model_dm.save('./Doc2Vec/20newsgDoc2vec_DM_trained.model')
    print('Saved Doc2Vec models to Doc2Vec folder...')
    print ('...')
    
    # save the doc2vec representationsof each document to npy 
    np.save('./npy/doc2vec_dbow_rep.npy',model_dbow.docvecs.vectors_docs)
    np.save('./npy/doc2vec_dm_rep.npy',model_dm.docvecs.vectors_docs)
    print('Saved Doc2Vec representations to npy folder...')
    print ('...')

    print ('Doc2Vec models built and trained...')
    print ('...')
    print ('Features dimensions reducing with t-SNE in progress')
    print ('...')
    tsne = TSNE(n_components=2)
    
    # t-SNE the top 10000 documents
    DBOW_tsne = tsne.fit_transform(model_dbow.docvecs.vectors_docs[:10000])
    DM_tsne = tsne.fit_transform(model_dm.docvecs.vectors_docs[:10000])

    # data frame of distributed bags of words & distributed memory 
    df_dbow = pd.DataFrame(DBOW_tsne, columns=['First Component','Second Component'])
    df_dm = pd.DataFrame(DM_tsne, columns=['First Component','Second Component'])

    # DBOW figureS
    ax1 = df_dbow.plot.scatter(x = 'First Component', y='Second Component', c='DarkBlue')
    fig1 = ax1.get_figure()
    fig1.savefig('./Doc2Vec/doc2vec_bow.png')
    
    # DM figure 
    ax2 = df_dm.plot.scatter(x = 'First Component', y='Second Component', c='DarkBlue')
    fig2 = ax2.get_figure()
    fig2.savefig('./Doc2Vec/doc2vec_tfidf.png')

    print ('Plotted figure saved...')    
