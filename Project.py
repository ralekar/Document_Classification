import nltk,re,pprint
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import operator
import sys


def FrequencyDistribution(word,frequency):
    '''Distributing the Synsets the Frequency of the Words'''

    global flag

    SynsetList=[]
    word=wn.synsets(word)
    for wrd in word:
        wrd=str(wrd)
        string=re.search('\(\"',wrd)
        if string:
            doubleq=re.sub('Synset\(\"','',wrd)
            doubleq=re.sub('\"\)','',doubleq)
            SynsetList.append(doubleq)
        else:
            singleq=re.sub('Synset\(\'','',wrd)
            singleq=re.sub('\'\)','',singleq)
            SynsetList.append(singleq)
            
    length=len(SynsetList)
    try:
  
        distribution=float(frequency/length) #Dividing the Frequencies

        if flag==0:
            TrainedHashMap(SynsetList,distribution) #In the Trained Hash Map
           
        else:
            TestHashMap(SynsetList,distribution) # In the Test Hash Map
            
    except ZeroDivisionError:
                temp=10

    


def TrainedHashMap(SynsetList,distribution):
    '''Storing the Values of Synset and Creating a Key Value Pair'''
    
    global TrainedMap
    for syn in SynsetList:
         if syn in TrainedMap:
             val=TrainedMap[syn]
             TrainedMap[syn]=distribution+val #Updating the  Value of the Synsets
         else:
             TrainedMap[syn]=distribution
             


def TestHashMap(SynsetList,distribution):
    '''Storing the Values of Synset and Creating a Key Value Pair'''
    global TestMap
    for syn in SynsetList:
         if syn in TestMap:
             val=TestMap[syn]
             TestMap[syn]=distribution+val
         else:
             TestMap[syn]=distribution
             
    
    
def SimilarityDistance():
    
    global TrainedMap
    global TestMap
    NetworkFlow=[]
    for TrainSyn in TrainedMap:
        TrainSyn=str(TrainSyn)
        Demand=float(TrainedMap[TrainSyn]) # Demand from the Trained Document
        TrainSyn=wn.synset(TrainSyn)
        for TestSyn in TestMap:
                TestSyn=str(TestSyn)
                Supply=float(TestMap[TestSyn]) # Supply From the Test Document
                TestSyn=wn.synset(TestSyn)
                Path=str((TrainSyn.path_similarity(TestSyn)))
                if Path!='None':
                    SemanticDistance=float(Path)
                    DistributionalMeasure=Supply-Demand #Minimum Cost Flow
                    NetworkFlow.append(float(SemanticDistance*DistributionalMeasure)) #Earth Movers Distance
    print '\nThe Earth Mover Distance :',sum(NetworkFlow)                           
    

def Treatment(ReadLines):
    '''Removing the Stop words and creating a Frequency Distribution List
    of Words in the Document'''
    global flag
    tokens=nltk.word_tokenize(ReadLines)
    StopWords=stopwords.words('english')
    newTokens=[]
    Text=[]

    for t in tokens:
        if t.isalpha() and t!='n':
           newTokens.append(t.lower())
    for nt in newTokens:
        temp=0
        for st in StopWords:
            if st==nt:
                temp=1
        if temp==0:
            Text.append(nt)
    if flag==1:
        print '\n@@@@@@Test Document Statisitcs@@@@@@'
    else:
        print '\n@@@@@@Trained Document Statistics@@@@@@'

    Tokens=nltk.FreqDist(Text)
    print '\nTotal Number of Words : ',len(tokens)
    print '\nNumber of Words for Comparison: ',len(Tokens)
    print '\nTotal Number of Stop Words: ',len(tokens)-len(Text)
    for tk in Tokens:
        freq=float(Tokens[tk])
        FrequencyDistribution(tk,freq)
        

def FileRead(files):
    '''Read lines from the File'''
    files=str(open(files,'r').readlines())
    Treatment(files)
    
                        
def main():
    
    global TrainedMap
    global TestMap
    global flag

    TrainedMap={}
    TestMap={}
    flag=0

    FileRead(sys.argv[1])
    flag=1
    FileRead(sys.argv[2])
    SimilarityDistance()


       
    
if __name__=='__main__':
    main()

    
   
    
