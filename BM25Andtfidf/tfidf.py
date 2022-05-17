
import math
from Assignment1_Q1 import parse_rcv_coll,parse_query


#Task 2.1
def calc_df(col):
    """
    Create the documents frequency
    Input: 
    col: the collection of the bag of words (dictionary)
    return:
    the document frequency dictionalry
    """
    df = {}
    for id, doc in col.doc_coll.items():
        for term, fre in doc.getTerm().items():
            try:
                df[term] += 1
            except KeyError:
                df[term] = 1
    df = {k: v for k, v in sorted(df.items(), key=lambda item: item[1], reverse=True)}
    return df
#Task 2.2
def tfidf(doc, df, ndocs):
    """
    for the tfidf equation: We use the smoothing equation from the lecture note and assignment instruction
    input:
    doc: document object (BOW)
    df: document frequency (Dictionary)
    ndocs: total number of document
    return:
    tfidf_dict: the dictionary of tfidf
    """
    tfidf_dict = {}
    totalsqrd = 0
    for term, ter_freq in doc.term.items():
        totalsqrd+= pow((math.log10(ter_freq)+1) * math.log10(ndocs/df[term]),2)
    totalsqrd = pow(totalsqrd,0.5) # The smoothing term for Tfidf

    for term,freq in doc.term.items():
        tfidf_dict[term] = ((math.log10(freq)+1)*math.log10(ndocs/df[term]))/ totalsqrd # Tfidf formular

    tfidf_dict = {k: v for k, v in sorted(tfidf_dict.items(), key=lambda item: item[1], reverse=True)}

    return tfidf_dict

## Task 2.3 calculate and ranking the document
def rankDocument(tfidfColl,query):
    """
    the ranking document function
    input:
    tfidfColl: the dictionaty of the tfidf for all document
    query: the term frequency of query
    return:
    ranking: the dictionary of ranking

    """
    ranking = {}

    for id,tfi in tfidfColl.items():
        values_rank = 0
        for term, tf in query.items():       
            try:
                values_rank += tfi[term] *tf # The documents weight is calculate the number of weight from tfidf with the frequency of the query
                ranking[id] =values_rank
            except:
                continue
        ranking[id] =values_rank
    ranking = {k: v for k, v in sorted(ranking.items(), key=lambda item: item[1], reverse=True)}
    return ranking

def tfQuery(qDict): # We have this option to calculate the weight of the query. the weight of each word is different we need to calculate teh term frequency for the query
    """
    Calculate term frequncy for query
    input:
    qDict: the query dictionary from parese_qurey
    return:
    tf_q: the dictionary of query weight
    """

    len_t = 0
    tf_q = {}
    for value in qDict.values():
        len_t +=value
    for keys,value in qDict.items():
        tf_q[keys] = value/len_t
    return tf_q


if __name__ == '__main__':

    # file path need to be change
    filepath = "C:\\Users\\n10677976\\OneDrive - Queensland University of Technology\\IN27\\S2Y2\\IFN647\\Assignment\\Assignment1\\"

    # stopword
    stopwords_f = open(filepath+'common-english-words.txt', 'r') # wk3
    stop_words = stopwords_f.read().split(',')
    stopwords_f.close()

    #Define variable
    tf_idf_coll = {} # tfidf collection
    indicator = 0
    queryTest = ["BELGIUM: MOTOR RACING-LEHTO AND SOPER HOLD ON FOR GT VICTORY."
    ,"UK: GOLF-BRITISH OPEN FOURTH ROUND LEADERBOARD.",
    "CANADA: Toronto stocks open mixed and directionless"] # Query testing
    #Create the collection
    coll = parse_rcv_coll(filepath+"Rnews_v1\\",stop_words)
    doc_coll = coll.doc_coll
    doc_fre = calc_df(coll)
    queryTf= []
    ranking =[]

    #Create the tfidf collection 
    for id, obs in doc_coll.items():
        tf_idf_coll[id] = tfidf(obs,doc_fre,coll.getDocNum())
    #Query term
    #Create the ranking colection from query
    for i in queryTest:
        queryTf.append(parse_query(i,stop_words))
    for i in queryTf:
        ranking.append(rankDocument(tf_idf_coll,i))
    
    #Create the ranking colection from query
    for i in queryTf:
        ranking.append(rankDocument(tf_idf_coll,i))

    # Writing the document
    with open(filepath+'result\\Arnutt_Kanchanatavee_Q2.txt', 'w') as f:
        for id, ob in doc_coll.items():
            ob_doc = doc_coll[id]
            tfidf_dict = tfidf(ob_doc,doc_fre,coll.getDocNum())
            first12pair = {k: tfidf_dict[k] for k in list(tfidf_dict)[:12]} #Stackoverflow code
            f.writelines(f"\nDocument {id} contains {ob.getNumTerm()}\n")
            for k,v in first12pair.items():
                f.writelines(f"{k}:{v}\n")
        for i in queryTest:      
            f.writelines(f"\nThe Ranking Result for query: {i} \n")
            for id,score in ranking[indicator].items():
                f.writelines(f"{id}, {score} \n")
            indicator+=1

        
        


