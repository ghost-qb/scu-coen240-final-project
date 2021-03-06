"""
Santa Clara University

COEN 240 - Machine Learning

Final Project

Quan Bach
Anh Truong



By running thi file:
    - a support vector machine will perform classification based on tf-idf representation
    - performance scores will be shown in the output 
    
    
    
*** NOTICE ***: this script will dowload the 20 news group dataset from sklearn and perform processing directly here before the models. 
Therefore, it does not used the vocabularies generated by other files previously. However, the content should be the same. 


"""
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.cluster import normalized_mutual_info_score as nmi
from sklearn.svm import LinearSVC
from sklearn import metrics
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
        
    print('Classification with SVM in progresss')    
    # store training feature matrix
    X_train = train_vectors
    # store training response
    y_train = newsgroup_train.target
    
    # store testing feature matrix 
    X_test = test_vectors
    # store testing response vector 
    y_test = newsgroup_test.target
    
    
    # Implementing classification model using Linear Support Vectors Classifier
    svm = LinearSVC()
    
    # train the model with train data
    svm.fit(X_train, y_train)
    
    # predict the response for new data i.e. test data
    y_predict = svm.predict(X_test)
    
    # predict the resposne score for test data
    y_predict_score_svc = svm.decision_function(X_test)
    
    # out put learned information 
    print ('Predicted Class labels: ', y_predict)
    print ('Predicted Score: \n', y_predict_score_svc)
    
    # Print evalulation 
    print()
    print('----------Performance metrics----------')
    print(metrics.classification_report(y_test, y_predict, target_names=newsgroup_test.target_names))
    print ()
    print('----------Confusion Matrix----------')
    print(metrics.confusion_matrix(y_test,y_predict))
    print()
    print ('NMI Score: ', nmi(y_test,y_predict))
    print('Classification Error of SVM: ', 1 - metrics.accuracy_score(y_test,y_predict))
    print('Sensitive of SVM: ', metrics.recall_score(y_test,y_predict, average='weighted'))
    print('Precision of SVM: ', metrics.precision_score(y_test,y_predict,average='weighted'))
    print('F-measure of SVM: ', metrics.f1_score(y_test,y_predict,average='weighted'))
    
    
    f, ax = plt.subplots(figsize=(16, 12))
    
    
    ax = sns.heatmap(metrics.confusion_matrix(y_test,y_predict), annot=True, cmap='Blues',annot_kws={"size":8})
    
    plt.savefig('svm_confusion_matrix.png')
    plt.show()
