
import math
from Assignment1_Q1 import parse_rcv_coll
from Assignment1_Q1 import parse_query
from Assignment1_Q2 import calc_df


def avgDoclen(coll):
    """
    Calculate the average document len from the coolection
    input:
    coll: the Bow collection
    return:
    the average document lenght 
    """
    totalDoclen=0
    for id, bow in coll.doc_coll.items():
        totalDoclen += bow.getDocLen()
    return totalDoclen/coll.getDocNum()

def bm25(coll, q, df):
    """
    BM25 function is to calcuate the score of the relevent query to the eocument
    input:
    coll: the object of the bag of word collection 
    q: query that has been pre-process by parse_query function
    df: the document frequency
    return:
    bm25s: the dictionary of bm25 score
    """
    bm25s = {}
    avg_dl = avgDoclen(coll)
    no_docs = coll.getDocNum()
    for id, doc in coll.doc_coll.items():
        bm25_ = 0.0
        k = 1.2 * ((1 - 0.75) + 0.75 * (doc.docLen / float(avg_dl)))
        for qt,qf in q.items(): # Dictionary
            n = 0
            bm= 0
            if qt in list(df.keys()):
                n = df[qt]
                try:
                    f = doc.term[qt]
                    bm = math.log2((1/((n + 0.5)/(no_docs - n + 0.5)))) * (((1.2 + 1) * f) / (k + f)) * (((100 + 1) * qf) / float(100 + qf))
                    bm25_ += bm
                except:
                    bm25_ += bm
        bm25s[id] = bm25_
    bm25s = {k: v for k, v in sorted(bm25s.items(), key=lambda item: item[1], reverse=True)}
    return bm25s

if __name__ == '__main__':

    # file path need to be change
    filepath = "C:\\Users\\n10677976\\OneDrive - Queensland University of Technology\\IN27\\S2Y2\\IFN647\\Assignment\\Assignment1\\"

    # stopword
    stopwords_f = open(filepath+'common-english-words.txt', 'r') # wk3
    stop_words = stopwords_f.read().split(',')
    stopwords_f.close()

    #Create the collection
    coll = parse_rcv_coll(filepath+"Rnews_v1\\",stop_words)
    doc_coll = coll.getDocCol()
    
    # query process
    test_querylist = ["This British fashion","All fashion awards","The stock markets","The British-Fashion Awards"]
    query_dict =[]
    for i in test_querylist:
        query_dict.append(parse_query(i, stop_words))

    #Average document lenght 
    avg_doclen = avgDoclen(coll)

    #Document frequency 
    doc_freq = calc_df(coll)

    # BM25
    all_bm25_ranking = []
    numberlist = 0
    for query in query_dict:
        bm25Dict = bm25(coll,query,doc_freq)
        all_bm25_ranking.append(bm25Dict)
    # Writing the document
    with open(filepath+'result\\Arnutt_Kanchanatavee_Q3.txt', 'w') as f:
        f.writelines(f"Average document length for this collection is: {avg_doclen}\n")
        for i in test_querylist:
            f.writelines(f"\nThe query is:: {i}\n")
            f.writelines(f"The following are the BM25 score for each document:\n")
            for id, score in all_bm25_ranking[numberlist].items():
                f.writelines(f"Document ID:{id} , Doc Length: {doc_coll[id].docLen} -- BM25 Score: {score}\n")
            f.writelines("\nThe following are possibly relevant documents retrieved -\n")
            temp = {k: v for k, v in sorted(all_bm25_ranking[numberlist].items(), key=lambda item: item[1], reverse=True)}
            for id,score in temp.items():
                f.writelines(f"Doc Id: {id} - Score: {score}\n")

            numberlist+=1

