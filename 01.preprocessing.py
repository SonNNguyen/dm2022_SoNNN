import csv
import math
def TF(word_count, words_document):
    # word_count count of all words
    # words_document one doc to count
    # print("here")
    TF = dict()
    # print("words_document ", len(words_document))
    for word, count in word_count.items():
        # print("count: ",count)
        # print("word: ", word)
        TF[word] = count/len(words_document)
        # print("TF[word] ", TF[word])
    return TF

def DF (word, allDocuments):
    
    count = 0 
    for doc in allDocuments:
        if word in doc:
            count +=1 #D(w)
    
    return count/len(allDocuments)

def IDF (word, DF):
    return math.log10(1/DF)

with open('text.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=' ')
    
    rows = []
    for row in csv_reader:
        rows.append(row)    #each row is a document

    print('Processed {} lines.'.format(len(rows)))

    print("====")
    totalWords =set()
    # allWord_count = dict()
    TF_total = {}
    
    for doc_words in rows:
        totalWords = set(doc_words).union(totalWords)
        
        # allWords = set(doc_words)

    allWord_count={}
    # allWord_count.fromkeys(allWords, 0) 
    # print('allWord_count ', allWord_count)
    # Counting all words
    for word in totalWords:
        if word not in allWord_count:
            allWord_count[word] = 0
        allWord_count[word]+=1 #counting


    DF_total = {}

    for i in totalWords:
        DF_total[i]= DF(i, rows)

    # print('DF_total ', DF_total)

    # frequency of each word
    for doc_words in rows:

        TF_this = TF(allWord_count, doc_words)

        for i in doc_words:
            
            TF_IDF= IDF(i, DF_total[i])*TF_this[i]
            print("Word: '{}' TF_IDF: '{}' ".format(i, TF_IDF))

