from xml.dom import minidom
from .conversation import Conversation
import os

def xml2csv(nameXML,nameCSV,predatorsCSV):
    if not (isinstance(nameXML,str) and isinstance(nameCSV,str) and isinstance(predatorsCSV,str)):
        raise Exception('params must be a string')
    
    if not os.path.exists(nameXML):
        raise Exception('XML not found')

    if not os.path.exists(predatorsCSV):
        raise Exception('Predators CSV not found')
    

    predators = []
    with open(predatorsCSV) as f:
        lines= f.readlines()
        for line in lines:
            predators.append(line.rstrip())
    #print(predators)
    doc = minidom.parse(nameXML)
    conversations = doc.getElementsByTagName('conversation')
    count =0

    
    with open(nameCSV, 'w', encoding="utf-8") as the_file:
    
        for conversation in conversations:
            
            if conversation.hasAttribute("id"):
                
                conversation_id = conversation.getAttribute("id")

                con_csv = Conversation(str(conversation_id))            
                messages = conversation.getElementsByTagName('message')
                authors = set()
                list_messages = []                       
                for message in messages:                
                    authors.add(message.getElementsByTagName('author')[0].childNodes[0].data)
                    try:

                        list_messages.append(removechars(str(message.getElementsByTagName('text')[0].childNodes[0].data)))
                    except Exception as e:        
                        continue 
                
                list_authors = list(authors)
                con_csv.set_authors(list_authors)
                con_csv.set_messages(list_messages)

                for a in list_authors:
                    if a in predators:
                        con_csv.set_has_abusers(True)                        

                the_file.write(str(con_csv)+'\n')
                if len(authors) > 2:
                    count +=1
                    #print(str(con_csv))`
                
    #print("Len of conversations with more than 2 authores: " + str(count))
    return


def removechars(words):
    words2erase = [';','|','\\','\r','\n']
    words = words.rstrip()
    for w in words2erase:
        words=words.replace(w,'')
    return words