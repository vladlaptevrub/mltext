import pandas
import pymorphy2 as pymorphy2
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from django.conf import settings
import os

def normalize_string(old_string):
    #print(old_string)
    morph = pymorphy2.MorphAnalyzer()
    new_string = ''
    words = old_string.split(" ")
    i = 0
    for word in words:
        for new_word in morph.normal_forms(word):
            new_string += new_word + ' '

    #print("NORM STRING")
    #print(new_string)
    return new_string

def sw_cleaning(old_string, sw_list):
    new_string = ''
    clean = 1
    words = old_string.split(" ")
    for w in words:
        for word in sw_list:
            if (w == word):
                clean = 0
        if (clean == 1):
            new_string += w + ' '
        else:
            clean = 1

    #print("SW CLEAN STRING")
    #print(new_string)
    return new_string

def sym_cleaning(old_string, sym_list):
    #print("OLD STRING")
    #print(old_string)
    new_string = ''
    clean = 1
    for s in old_string:
        for sym in sym_list:
            if (s == sym):
                clean = 0
        if (clean == 1):
            new_string += s
        else:
            clean = 1

    #print("SYM CLEAN STRING")
    #print(new_string)
    return new_string



def classify(is_sw, stop_words, is_sym, symbols, is_norm, test_data, labels, classifier_id):

    vectorizer = CountVectorizer(analyzer="word", tokenizer=None, preprocessor=None, stop_words=None, max_features=5000)
    if (is_sym == 1):
        if (is_norm == 1):
            if(is_sw == 1):
                print("Start preliminary procsessing: SYM, NORM, SW")
                td = list()
                for sentace in test_data:
                    td.append(sw_cleaning(normalize_string(sym_cleaning(sentace, symbols)), stop_words))
            else:
                print("Start preliminary procsessing: SYM, NORM")
                td = list()
                for sentace in test_data:
                    td.append(normalize_string(sym_cleaning(sentace, symbols)))
        else:
            if (is_sw == 1):
                print("Start preliminary procsessing: SYM, SW")
                td = list()
                for sentace in test_data:
                    td.append(sw_cleaning(sym_cleaning(sentace, symbols), stop_words))
            else:
                print("Start preliminary procsessing: SYM")
                td = list()
                for sentace in test_data:
                    td.append(sym_cleaning(sentace, symbols))
    else:
        if (is_norm == 1):
            if(is_sw == 1):
                print("Start preliminary procsessing: NORM, SW")
                td = list()
                for sentace in test_data:
                    td.append(sw_cleaning(normalize_string(sentace), stop_words))
            else:
                print("Start preliminary procsessing: NORM")
                td = list()
                for sentace in test_data:
                    td.append(normalize_string(sentace))
        else:
            if (is_sw == 1):
                print("Start preliminary procsessing: SW")
                td = list()
                for sentace in test_data:
                    td.append(sw_cleaning(sentace, stop_words))
            else:
                print("Skip preliminary procsessing")
                td = test_data

    #fb = open('dataset.csv', encoding='utf-8')
    fb = open(os.path.join(settings.PROJECT_ROOT, 'dataset.csv'), encoding='utf-8')
    csv_data_b = pandas.read_csv(fb, sep=',', skiprows=[0], header=None)

    my_list_text = list()
    my_list_types = list()
    i = 0

    print("Start reading dataset")

    while i < 10000:
        item = csv_data_b[0][i]
        type = csv_data_b[1][i]
        my_list_text.append(item)
        my_list_types.append(type)
        i += 1

    print("Start vectorizing data")
    counts = vectorizer.fit_transform(my_list_text)

    tf_transformer = TfidfTransformer(use_idf=False).fit(counts)

    v = tf_transformer.transform(counts)

    #dataset = dataset.toarray()

    print("Start vectorizing test_data")
    new_counts = vectorizer.transform(td)
    new_v = tf_transformer.transform(new_counts)

    if (classifier_id == "f"):
        print("Random Forest is chosen")
        classifier = RandomForestClassifier(n_estimators=100)
        print("Start build model")
        classifier = classifier.fit(v.toarray(), my_list_types)
    elif(classifier_id == "nb"):
        print("NaiveB is chosen")
        classifier = GaussianNB()
        print("Start build model")
        classifier = classifier.fit(v.toarray(), my_list_types)
    elif(classifier_id == "knn"):
        print("KNeighbors is chosen")
        classifier = KNeighborsClassifier()
        print("Start build model")
        classifier = classifier.fit(v.toarray(), my_list_types)
    elif(classifier_id == "svm"):
        print("SVM is chosen")
        classifier = SVC()
        print("Start build model")
        classifier = classifier.fit(v.toarray(), my_list_types)
    elif(classifier_id == "dtrees"):
        print("Decision Tree is chosen")
        classifier = DecisionTreeClassifier()
        print("Start build model")
        classifier = classifier.fit(v.toarray(), my_list_types)
    else:
        print("NaiveB is chosen")
        classifier = GaussianNB()
        print("Start build model")
        classifier = classifier.fit(v.toarray(), my_list_types)

    print("Start Prediction")
    predicted = classifier.predict(new_v.toarray())

    step = 0
    counter = 0

    for a in predicted:
        if (a == labels[step]):
            counter += 1
        step += 1

    print("RESULT:", counter/step*100, "%")

    return (counter)





