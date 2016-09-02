from flask import Flask, url_for, request
app = Flask(__name__)
import json
import os
import requests

username = "f863efbd-a2f3-4d09-b35f-bf4bb6d2a758-bluemix"
password = "227d1f47724f987ad94c881073c43459a733587730047a1cbe61998f347e2e0a"
baseUrl = "https://{0}.f863efbd-a2f3-4d09-b35f-bf4bb6d2a758-bluemix:227d1f47724f987ad94c881073c43459a733587730047a1cbe61998f347e2e0a@f863efbd-a2f3-4d09-b35f-bf4bb6d2a758-bluemix.cloudant.com/{1}"

@app.route('/questions/createQuestion', methods = ['POST'])
def api_createQuestion():
    if 'newQuestion' in request.args and 'DBname' in request.args and 'docId' in request.args and 'newID' in request.args:
                     #username = "18bfab56-5fa2-48ff-a4f5-165198d51978-bluemix"
                     #password = "00aac17798d9a4cf1728f6078f5e04d708bb6a7c96f03e9e657f82074e301729"
                     db_name =  request.args["DBname"]
                     QuestionID = request.args["newID"]
                     Question = request.args["newQuestion"]
                     baseUri = baseUrl.format(username, db_name)
                     creds = (username, password)
                     docId = request.args["docId"]
                     response = requests.get(
                    "{0}/{1}".format(baseUri, docId),
                    auth=creds
                    )
                     doc = response.json()
                     if QuestionID in doc["ID"].values():
                        return '[U] ID ' + str(QuestionID) + "[U] already in question bank."
                     print("The document's rev is {0}".format(doc["_rev"]))
                     doc['ID']["ID" + str(QuestionID) ] = QuestionID
                     doc['Question']["Question" + str(QuestionID)] = Question
            
                     response = requests.put(
                     "{0}/{1}".format(baseUri, docId),
                     data=json.dumps(doc),
                     auth=creds
                     )
                     rev2 = response.json()['rev']
                     print("The document's new rev is {0}".format(rev2))
                     print ("Written Data in Document\n")
                     return '[U] Creating question' +  str(QuestionID) + " " + request.args['newQuestion']
    else:
            return '[U] NOT Creating the question' 

## delete Questions
@app.route('/questions/deleteQuestionById', methods = ['DELETE'])
def api_deleteQuestionById():
    if 'questID' in request.args:
                    #username = "raggarw1"
                    #password = "My_password"
                    db_name =  request.args["DBname"]
                    baseUri = baseUrl.format(username, db_name)
                    creds = (username, password)
                    docId = request.args["docId"]
                    questID = request.args["questID"]
                    QuestionKey = str("Question") + str(questID)
                    IDKey = str("ID") + str(questID)
                    response = requests.get(
                    "{0}/{1}".format(baseUri, docId),
                    auth=creds
                    )
                    doc = response.json()
                    del doc["Question"][QuestionKey]
                    del doc["ID"][IDKey]
                    response = requests.put(
                    "{0}/{1}".format(baseUri, docId),
                    data=json.dumps(doc),
                    auth=creds
                    )
                    rev2 = response.json()['rev']
                    print("The document's new rev is {0}".format(rev2))
                    return '[U] Deleted question: ' + questID
    else:
                    return '[U] NOT Deleting the question ' + questID
  #### get all Questions
@app.route('/questions/getAllQuestions')
def api_getAllQuestions():
    if 'DBname' in request.args and 'docId' in request.args:
                    #username = "raggarw1"
                    #password = "My_password"
                    db_name =  request.args["DBname"]
                    baseUri = baseUrl.format(username, db_name)
                    creds = (username, password)
                    docId = request.args["docId"]
                    response = requests.get(
                    "{0}/{1}".format(baseUri, docId),
                    auth=creds
                    )
                    doc = response.json()
                    id_list_str = [val[8:] for val in doc["Question"].keys()]
                    id_list_int = [int(val) for val in id_list_str]
                    quest_list = doc["Question"].values()
                    indexed_quest_list = zip(["Q No." + str(val) + " " for val in id_list_int], quest_list)
                    
                                            
                    print(indexed_quest_list)
                    return '[A] List of all questions in the DB:\n'
    else:
                    return '[U] NOT printing the question bank' 
  #### Get questions by ID
  
@app.route('/questions/getQuestionById')
def api_getQuestionById():
                    #username = "raggarw1"
                    #password = "My_password"
                    db_name =  request.args["DBname"]
                    baseUri = baseUrl.format(username, db_name)
                    creds = (username, password)
                    docId = request.args["docId"]
                    questID = request.args["questID"]
                    response = requests.get(
                    "{0}/{1}".format(baseUri, docId),
                    auth=creds
                    )
                    doc = response.json()
                    QuestionKey = str("Question") + str(questID)
                    Question = doc["Question"][QuestionKey]
                    return '[U] This is the question \n'  + Question                              

port = os.getenv('VCAP_APP_PORT', '5000')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))