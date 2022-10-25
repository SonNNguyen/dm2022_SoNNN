import csv

def TF(word_count, words_document):
    # word_count count of all words
    # words_document one doc to count
    TF = dict()
    for word, count in word_count.items():
        TF[word] = count/len(words_document)
    return TF

with open('text.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=' ')
    line_count = 0
    rows = []
    for row in csv_reader:
        rows.append(row)    #each row is a document

    print('Processed {} lines.'.format(len(rows)))

    print("====")
    # allWords =set()
    for doc_words in rows:
        # allWords = set(doc_words).union(allWords)
        allWords = set(doc_words)

    
        allWord_count = dict.fromkeys(allWords, 0) 
        
        # Counting all words
        for word in doc_words:
            allWord_count[word]+=1 #counting

        # frequency of each word
        TF = TF(allWord_count, doc_words)
    print(TF)

    # print("_________")
    # print (allWord_count)
    # TF = TF(allWord_count, rows)    #each row is a document
    # print("++++++++++")
    # print(TF)