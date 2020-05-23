
import networkx as nx
import numpy as np
 
from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
import math
import statistics
from tkinter import *
import sys
from pathlib import Path
import os
import tkinter.messagebox




fileName=None
flag=False
flaf2=False

root = Tk()
root.title("Text Summarizition")
root.geometry("600x300")

ment=StringVar()
ment2=StringVar()






def Browes():
    global fileName
    global mEntry
    global flag
    fileName = filedialog.askopenfilename()
    mEntry.insert(0,fileName)
    if mEntry.get():
        flag=True
    return





def remove_string_special_characters(s):
    str=re.sub('[^\w\s]','',s)
    srtr=re.sub('_','',str)
    str=re.sub('\s+',' ',str)
    str=str.strip()
    return str

def get_doc(sent):
    doc_info=[]
    i=0
    for sents in sent:
        i+=1
        count=count_words(sents)
        temp={'doc_id':i,'doc_length':count}
        doc_info.append(temp)
    return doc_info

def count_words(sent):
    count=0
    words=word_tokenize(sent)
    for word in words:
        count+=1
    return count

def create_freq_dict(sents):
    i=0
    freqDict_list=[]
    for sent in sents:
        i+=1
        freq_dict={}
        words=word_tokenize(sent)
        for word in words:
            if word in freq_dict:
                freq_dict[word]+=1
            else:
                freq_dict[word]=1
            temp={'doc_id' : i, 'freq_dict':freq_dict}
        freqDict_list.append(temp)
    return freqDict_list
    
def computeTF(doc_info,freqDict_list):
    TF_Scores=[]
    for tempDict in freqDict_list:
        id=tempDict['doc_id']
        for k in tempDict['freq_dict']:
            temp={'doc_id':id,'TF_Score':tempDict['freq_dict'][k]/doc_info[id-1]['doc_length'],'key':k}
            TF_Scores.append(temp)
    return TF_Scores

def computeIDF(doc_info,freqDict_list):
    IDF_Scores=[]
    counter=0
    for dict in freqDict_list:
        counter+=1
        for k in dict['freq_dict'].keys():
            count=sum([k in tempDict['freq_dict'] for tempDict in freqDict_list])
            temp={'doc_id':counter,'IDF_Score': math.log(len(doc_info)/count), 'key':k}
            IDF_Scores.append(temp)
    return IDF_Scores

def computeTFIDF(TF_Scores,IDF_Scores):
    TFIDF_Scores=[]
    for j in IDF_Scores:
        for i in TF_Scores:
            if j['key']==i['key'] and j['doc_id']==i['doc_id']:
                temp={'doc_id':j['doc_id'],'TFIDF_Scores':j['IDF_Score']*i['TF_Score'],'key':i['key']}
        TFIDF_Scores.append(temp)
    return TFIDF_Scores

def get_sent_score(TFIDF_Scores,text_sents,doc_info):
    sentence_info=[]
    for doc in doc_info:
        sent_score=0
        for i in range(0,len(TFIDF_Scores)):
            temp_dict=TFIDF_Scores[i]
            if doc['doc_id']==temp_dict['doc_id']:
                sent_score+=temp_dict['TFIDF_Scores']
        temp={'doc_id':doc['doc_id'],'sent_score':sent_score,'sentence':text_sents[doc['doc_id']-1]}
        sentence_info.append(temp)
    return sentence_info

       

def get_summary(sentence_info):
    sum=0
    summary=[]
    array=[]
    for temp_dict in sentence_info:
        sum+=temp_dict['sent_score']
    avg=sum/len(sentence_info)
    for temp_dict in sentence_info:
        array.append(temp_dict['sent_score'])
    stdev=statistics.stdev(array)
    for sent in sentence_info:
        if(sent['sent_score'])>=avg+stdev:
            summary.append(sent['sentence'])
    summary='\n'.join(summary)
    return summary

def Summarization():
    global mEntry
    global mEntry2
    global flag
    global fileName
    global ment2
    if not ment2.get():
        return tkinter.messagebox.showinfo("Eror","Enter number of Rows")
    if not ment2.get().isdigit():
        return tkinter.messagebox.showinfo("Eror","Invalid entry")
    if int(ment2.get())<=0:
        return tkinter.messagebox.showinfo("Eror","Invalid entry")
    if flag:
        f=open(fileName,'r')
        print(fileName)
        document=f.read()
        f.close()
        document = ' '.join(document.strip().split('\n'))
        sentence_tokenizer = PunktSentenceTokenizer()
        sentences = sentence_tokenizer.tokenize(document)
        print(sentences)
        c = CountVectorizer()
        bow_matrix = c.fit_transform(sentences)
        normalized_matrix = TfidfTransformer().fit_transform(bow_matrix)
        similarity_graph = normalized_matrix * normalized_matrix.T
        nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
        scores = nx.pagerank(nx_graph)
        ranked = sorted(((scores[i],s) for i,s in enumerate(sentences)),reverse=True)
        fileName=os.path.basename(fileName)
        text_file = open("Summary"+fileName, "w")
        for i in range(0,int(ment2.get())):
            if(i<len(ranked)):
                text_file.write(ranked[i][1])
                text_file.write('\n')
        text_file.close()
        mEntry.delete(0, END)
        mEntry2.delete(0, END)
        tkinter.messagebox.showinfo("Eror","Done")
        
        
    else:
        tkinter.messagebox.showinfo("Eror","First load fies")

button1=Button(root,text="Browes",command=Browes).place(x=500,y=50)#Browes
mEntry=Entry(root,width=50,textvariable=ment)#Directory Path
mEntry.place(x=180,y=55)
label=Label(root,text="Directory Path").place(x=80,y=55)
mEntry2=Entry(root,width=10,textvariable=ment2)#Rows
mEntry2.place(x=180,y=120)
label2=Label(root,text="Rows").place(x=80,y=120)
ranked=button3=Button(root,width=25,text="Summarization",command=Summarization).place(x=220,y=170)




