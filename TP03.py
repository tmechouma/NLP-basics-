# (c) MECHOUMA Toufik


import sys
import nltk
import pandas as pd
from pycorenlp import StanfordCoreNLP
from nltk.corpus import wordnet  as wn
import csv
import json

#instanciation de l'objet StanfordCoreNLP pour pouvoir utiliser ses methodes
nlp = StanfordCoreNLP('http://localhost:9000')

#****************************la fonction qui permet de faire l'extraction des dependances linguistiques*********************************
def getLingDep(phrase):
    texte = ''
    deps,listefinale = [],[]
    #faire un parsing des dependances linguistique et les faire sortir sous format JSON
    res = nlp.annotate(phrase, properties={'annotators':'depparse','outputFormat': 'json'})
    #Sauvegarde sous format JSON
    createJF(res)
    for e in res['sentences'][0]['enhancedPlusPlusDependencies']:
        d= "{0}({1},{2})".format(e['dep'],e['governorGloss'],e['dependentGloss'])
        deps.append(d)
    return(deps)
#**************************La fonction qui permet de faire la lemmatisation*************************************************************
def getLemmas(text):
    #annotation et post tagging et l'extraction sous format JSON
    annot_doc = nlp.annotate(text,properties={'annotators': 'ner, pos','outputFormat': 'json','timeout': 1000,})
    parsed_text = {'word':[],'lemma':[]}
    for sentence in annot_doc["sentences"]:
        for word in sentence["tokens"]:
            parsed_text['word'].append(word["word"])
            parsed_text['lemma'].append(word["lemma"])
    # L'affichage avec DataFrame de Pandas 
    df = pd.DataFrame(parsed_text)
    print(df)
    # Sauvegarde sous format CSV
    saveFile(df.to_csv(index=False).split())
#**************************La fonction qui permet de faire le Post Tagging**************************************************************    
def getPos(text):         
    annot_doc = nlp.annotate(text,properties={'annotators': 'ner, pos','outputFormat': 'json','timeout': 1000,})
    parsed_text = {'word':[],'pos':[]}
    for sentence in annot_doc["sentences"]:
        for word in sentence["tokens"]:
            parsed_text['word'].append(word["word"])
            parsed_text['pos'].append(word["pos"])
    df = pd.DataFrame(parsed_text)
    print(df)
    saveFile(df.to_csv(index=False).split())
#*************************La fonction qui permet de faire la detection des entités renommées*******************************************    
def getNer(text):
    annot_doc = nlp.annotate(text,properties={'annotators': 'ner, pos','outputFormat': 'json','timeout': 1000,})
    parsed_text = {'word':[],'ner':[]}
    for sentence in annot_doc["sentences"]:
        for word in sentence["tokens"]:
            parsed_text['word'].append(word["word"])
            parsed_text['ner'].append(word["ner"])
    df = pd.DataFrame(parsed_text)
    print(df)
    saveFile(df.to_csv(index=False).split())
#*************************La fonction qui permet de sauvegarder les dependances linguistiques sous format JSON**************************
def createJF(dic):
    fn = input("Veuillez entrer le nom de fichier sans extension SVP :")
    json.dump(dic,open(fn+".txt",'w'))
    
#************************************************************************************************
def menu():
    print("--------------------------------(c) MECHOUMA Toufik--------------------------")
    print("*************************MENU************************************************")
    print('* 1 - aimerez vous extraitre  les hypernymes d\'un mot                       *')
    print('* 2 - aimerez vous extraitre  les synonymes d\'un mot                        *')
    print('* 3 - aimerez vous extraitre  les antonymes d\'un mot                        *')
    print('* 4 - aimerez vous mesurer la similarité entre deux mots                    *')
    print('* 5 - aimerez vous extraire les dependances linguistiques  d\'une phrase     *')
    print('* 6 - aimerez vous faire une lemmatisation   d\'une phrase                   *')
    print('* 7 - aimerez vous faire une PoS tagging   d\'une phrase                     *')
    print('* 8 - aimerez vous extraire les entités renommées   d\'une phrase            *')
    print('* 0 - aimerez vous quitter le programme ?                                   *')
    print("*****************************************************************************")
    print("")
    operations(input("Veuillez saisir un numéro correspondant a l'une des opération SVP :"))
#************************************************************************************************
def operations(arg):
    mots = []
    if arg == '1':
        saveFile(display(getHypernyms(entrer())))
        main()
    elif arg== '2':
        saveFile(display(getSynonyms(entrer())))
        main()
    elif arg == '3':
        saveFile(display(getAntonyms(entrer())))
    elif arg == '4':
        mots = list(entrer2())
        getSimilarity(mots[0],mots[1])
        main()
    elif arg == '5':
        displayDep(getLingDep(entrerphrase()))
        main()
    elif arg == '6':
        getLemmas(entrerphrase())
        main()
    elif arg == '7':
        getPos(entrerphrase())
        main()
    elif arg == '8':
        getNer(entrerphrase())
        main()
    elif arg =='0':
        print('Merci ...!')
        sys.exit()
    else :
        print("numéro invalide")
#************************************************************************************************
def entrer():
    mot= input("Veuillez saisir le mot SVP :")
    return mot
def entrer2():
    mot1= input("Veuillez saisir le mot1 SVP :")
    mot2= input("Veuillez saisir le mot2 SVP :")
    return (mot1,mot2)
def entrerphrase():
    ph= (input("Veuillez entrer une phrase SVP :\n"))
    for charactere in ph:
         if charactere in "()'.-_$£@:/\=&[]{}%§?,;#+*":
             ph= ph.replace(charactere,' ')
    return ph
#*************La fonction qui permet d'extraire les Hypernymes***********************************    
def getHypernyms(word):
    liste,s,r =[],[],[]
    word = wn.synset(word+'.n.01')
    liste = list(word.hypernym_distances())
    for elem in liste:
        s.append(list(elem)[0])
    s = list(set(s))
    for syn in s:
        for l in syn.lemmas():
            r.append(l.name())
    r.append('Le Nombre Total est des hypernymes egale :'+ str(len(s)))
    return r   
#*************La fonction qui permet d'extraire les Synonymes*************************************
def getSynonyms(syn) :
    s = []
    for syns in wn.synsets(syn):
        for l in syns.lemmas():
           s.append(l.name())
    s = list(set(s))
    s.append('Le Nombre Total est des synonymes egale :'+str(len(s)))
    return s
#************La fonction qui permet d'extraire les Antonymes**************************************
def getAntonyms(ant) :
    liste =[]
    for syn in wn.synsets(ant): 
        for l in syn.lemmas(): 
            if l.antonyms():
                liste.append(l.antonyms()[0].name())
    liste = list(set(liste))
    liste.append('Le Nombre Total est des antonymes egale :'+str(len(liste)))
    return liste
#************La fonction qui permet de mesurer la similarité entre deux mots**********************
def getSimilarity(mot1,mot2):
     sim=[]
     it1 = wn.synsets(mot1)
     it2 = wn.synsets(mot2)
     try:
          for s1 in it1:
               for s2 in it2:
                    if wn.wup_similarity(s1,s2) !=None:
                         sim.append(wn.wup_similarity(s1,s2))
          print("La similarité sémantique entre <%s> et <%s> est %f:"%(mot1,mot2,max(sim)))
     except nltk.corpus.reader.wordnet.WordNetError:
          pass # ignoer les mots qui n'existent pas dans le dictionnaire.
     return sim
#*************************************************************************************************
def display(liste):
    for l in liste:
        print(l)
    print('\n')
    return liste

def displayDep(liste):
    print("la racine est --->",liste[0])
    for i in liste:
        print(i)
        
#*************************************************************************************************
def saveFile(liste):
    r = input('---Voulez vous sauvegarder dans un fichier csv ?  Taper o ou bien n ---> :')
    if r =='o' or r== 'O': 
        nf = input('Merci de saisir le nom de fichier a sauvegarder sans extension :')
        with open(nf+'.csv','w+', newline='') as myfile:
            wr = csv.writer(myfile,delimiter=',')
            wr.writerow(liste)
        myfile.close()
    elif r == 'n' or 'N':
        print('Merci..!')
        sys.exit()
    else:
        print('**vous avez tapez un autre caractère, Au revoir**')
        main()
#*************************************************************************************************        
def main():
    menu()
#*************************************************************************************************    
if __name__== "__main__":
    main()
        






















