import glob
import string
from stemming.porter2 import stem

class BowDoc:

    def __init__(self,docID):
        self.docID = docID
        self.term = {}
        self.docLen = 0

    def getDocLen(self):
        """
        The length of document
        """
        return self.docLen
    
    def getTerm(self):
        """
        the get the tem frequency of document
        """
        self.sortTerm()
        return self.term
    
    def addTerm(self,word):
        """
        add term in to the dictionary
        """
        try:
            self.term[word] +=1
        except:
            self.term[word] =1        

    def sortTerm(self, reverse =True):
        """
        reverse: Set default as True to sort in decending order

        sort term dictionary function
        """
        sort_d = {k: v for k, v in sorted(self.term.items(), key=lambda item: item[1], reverse=reverse)}
        self.term = sort_d

    def getDocId(self):
        """
        Get Document ID
        """
        return self.docID

    def getDoc(self):
        """
        Get Document collection
        """
        return (self.docID,self.term)
    
    def getNumTerm(self):
        """
        Get total number of term
        """
        return len(self.term)
    
    def setDocLen(self,wordcount):
        """
        Set the document length
        """
        self.docLen = wordcount


class BowColl:
    """
    Instead of using Linked list, we use the object to create the collection
    """
    def __init__(self):
        self.doc_coll = {}


    def addDoc(self,doc):
        """
        input:
        docID: the document number
        term: term frequency of each document
        
        """
        self.doc_coll[doc.getDocId()] = doc
    
    def getDocCol(self):
        """
        get the collection
        """
        return self.doc_coll
    
    def getDocNum(self):
        """
        get total number of document
        """
        return len(self.doc_coll)
    


# Task 1.1
def parse_rcv_coll(inputpath, stop_words):
    """
    This fuction is to preprocess the information from the document,
    and store in to the bag of words object
    input:
    inputpath: The path of each document
    stop_words: list of english stop words

    return:
    the collection of the document in dictionary
    keys: the doocument number
    value: object of the document
    """
    
    coll = BowColl()
    for file in glob.glob(inputpath+"*.xml"): #for all xml file in the given directory
        start_end=False
        wordCount=0
        for line in open(file):
            line = line.strip()
            if start_end == False:
                if line.startswith("<newsitem"):
                    for part in line.split():
                        if part.startswith("itemid="):
                            doc_Id = part.split("=")[1].strip("\"")
                            curr_ob = BowDoc(doc_Id)
                            break
                if line.startswith("<text>"):
                    start_end=True
            elif line.startswith("</text>"):
                break
            else:
                line=line.replace("<p>","").replace("</p>","")
                line = line.translate(str.maketrans('',"",string.digits)).translate(
                    str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
                # The word is defined the that is not number, not in stopwords list and has length of charactor more than2
                for l in line.split():
                    wordCount +=1
                    l = stem(l.lower())
                    if l not in stop_words and len(l) >2:
                        curr_ob.addTerm(l)
                # Set document length
                curr_ob.setDocLen(wordCount)
                # Add object into word collection
                coll.addDoc(curr_ob)
    return coll

# Task 1.2
def parse_query(query0, stop_words_list):
    """
    query0: string for query expected to recieve from user
    stop_words_list: the list of English stop word
    
    """
    querylen =0 
    queryDict = {}
    query0 = query0.translate(str.maketrans('','',string.digits)).translate(str.maketrans(string.punctuation,' ' * len(string.punctuation)))
    for i in query0.split():
        if i.lower() not in stop_words_list and len(i) > 2:
            querylen = +1
            i = stem(i.lower())
            try:
                queryDict[i] += 1
            except:
                queryDict[i] =1

    return queryDict

if __name__ == '__main__':
    # filepath: need to be change 
    filepath = "C:\\Users\\n10677976\\OneDrive - Queensland University of Technology\\IN27\\S2Y2\\IFN647\\Assignment\\Assignment1\\"
    #Stop word
    stopwords_f = open(filepath+'common-english-words.txt', 'r') # wk3
    stop_words = stopwords_f.read().split(',')
    stopwords_f.close()
    # Testing query function
    queryInput = "Canada is next to the United State of America"
    querDict = parse_query(queryInput, stop_words)
    print(querDict)
    coll = parse_rcv_coll(filepath+"Rnews_v1\\",stop_words)
    doc_coll = coll.getDocCol() 
    with open(filepath+'result\\Arnutt_Kanchanatavee_Q1.txt', 'w') as f:
        for id, ob in doc_coll.items():
            f.writelines(f"\nDocument {id} contains {ob.getNumTerm()} terms and have total {ob.docLen} words\n")
            for k,v in ob.getTerm().items():
                f.writelines(f"{k}:{v}\n")

