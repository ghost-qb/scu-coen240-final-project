"""
Santa Clara University

COEN 240 - Machine Learning

Final Project

Quan Bach
Anh Truong

This is Part 8 of the Final Project 



By running thi file: 
    - the program will implement multinominal naieve bayesian classification on the dataset from tf-idf representation 
    - the performance scores will be shown in output 
    
    
    
*** NOTICE ***: this script will dowload the 20 news group dataset from sklearn and perform processing directly here before the lda models. 
Therefore, it does not used the vocabularies generated by other files previously. However, the content should be the same. 


"""
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.cluster import normalized_mutual_info_score as nmi
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
import matplotlib.pyplot as plt 
import seaborn as sns


if __name__ == '__main__':
    

    # fetching data from sklearn
    print('Loading data...')
    newsgroup_train = fetch_20newsgroups(subset='train', remove=('headers','footers','quotes'), shuffle=True)
    newsgroup_test = fetch_20newsgroups(subset='test', remove=('headers','footers','quotes'), shuffle=True)
    print('...')
    print('Data loaded...')
    print('...')
    print('Total train data: ', len(newsgroup_train.data))
    print('Total test data: ',len(newsgroup_test.data))
    
    
    
    # initialize vectors and get the train & test vectors 
    print('TF-IDF in progress...')
    print('...')
    vectorizer = TfidfVectorizer()
    train_vectors = vectorizer.fit_transform(newsgroup_train.data)
    test_vectors = vectorizer.transform(newsgroup_test.data)
    print('...')
    
    print('Classification with different classifiers in progresss')    
    # store training feature matrix
    X_train = train_vectors
    # store training response
    y_train = newsgroup_train.target
    
    # store testing feature matrix 
    X_test = test_vectors
    # store testing response vector 
    y_test = newsgroup_test.target
    
    # Initialize the estimator for KNN
    print('...')
    print('Classification with MNB in progress...')
    print('...')
    
    classifier_MNB = MultinomialNB(alpha=0.1)
    classifier_MNB.fit(X_train,y_train)
    
    # predict the response for new data
    y_predict = classifier_MNB.predict(X_test)
    print('Predicted Class labels: ', y_predict)
    
    # get the predict score 
    y_pred_score_mnb = classifier_MNB.predict_proba(X_test)
    print('Predicted Score: ', y_pred_score_mnb)
    
    # Print evalulation 
    print()
    print('----------Performance metrics----------')
    print(metrics.classification_report(y_test, y_predict, target_names=newsgroup_test.target_names))
    print ()
    print('----------Confusion Matrix----------')
    print(metrics.confusion_matrix(y_test,y_predict))
    print()
    print ('NMI Score: ', nmi(y_test,y_predict))
    print('Classification Error of MNB: ', 1 - metrics.accuracy_score(y_test,y_predict))
    print('Sensitive of MNB: ', metrics.recall_score(y_test,y_predict, average='weighted'))
    print('Precision of MNB: ', metrics.precision_score(y_test,y_predict,average='weighted'))
    print('F-measure of MNB: ', metrics.f1_score(y_test,y_predict,average='weighted'))
    
    
    f, ax = plt.subplots(figsize=(16, 12))
    
    
    ax = sns.heatmap(metrics.confusion_matrix(y_test,y_predict), annot=True, cmap='Blues',annot_kws={"size":8})
    
    plt.savefig('mnb_confusion_matrix.png')
    plt.show()