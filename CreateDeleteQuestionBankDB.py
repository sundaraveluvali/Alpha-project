from flask import Flask, url_for, request
app = Flask(__name__)
import json
import os
import requests
from datetime import datetime, timedelta

# Create Question Database
@app.route('/questions/createQuestionDB/<questiondb>')
def api_questionDB(questiondb):
    username = "f863efbd-a2f3-4d09-b35f-bf4bb6d2a758-bluemix"
    password = "227d1f47724f987ad94c881073c43459a733587730047a1cbe61998f347e2e0a"
    db_name = questiondb.lower()
    baseUri = "https://{0}.f863efbd-a2f3-4d09-b35f-bf4bb6d2a758-bluemix:227d1f47724f987ad94c881073c43459a733587730047a1cbe61998f347e2e0a@f863efbd-a2f3-4d09-b35f-bf4bb6d2a758-bluemix.cloudant.com/{1}".format(username, db_name)
    creds = (username, password)
    response = requests.put(
    baseUri,
    auth=creds     
    )
    response = requests.post(
    baseUri,
    data=json.dumps({"Question": {"Question0" : "Dummy"}, 
                     "ID": {"ID0" : 0}, 
                     "Read Flag" : {"Flag0" : 0}, 
                     "UserID" : {"UserID0": 0},
                     "PostDate" : {"PostDate0" : 99999999},
                     "Dum1" : {"Dum10": "Dummy"}}),
                     
    auth=creds,
    headers={"Content-Type": "application/json"}
)
    print( "Written Data in Document\n")

    docId = response.json()["id"]
    print ("The new document's ID is {0}".format(docId))
    print ("Created database at {0}".format(baseUri))
    return ('[C] Question DB Created ' + db_name)

# Delete Question Database
@app.route('/questions/deleteQuestionDB/<questiondb>')
def api_deleteQuestionDB(questiondb):
    username = "f863efbd-a2f3-4d09-b35f-bf4bb6d2a758-bluemix"
    password = "227d1f47724f987ad94c881073c43459a733587730047a1cbe61998f347e2e0a"
    db_name = questiondb
    baseUri = "https://{0}.f863efbd-a2f3-4d09-b35f-bf4bb6d2a758-bluemix:227d1f47724f987ad94c881073c43459a733587730047a1cbe61998f347e2e0a@f863efbd-a2f3-4d09-b35f-bf4bb6d2a758-bluemix.cloudant.com/{1}".format(username, db_name)
    creds = (username, password)
    response = requests.delete(
    baseUri,
    auth=creds
    )
    print( "Deleted database {0}".format(baseUri))
    return '[C] Deleted Question DB ' + db_name
   
port = os.getenv('VCAP_APP_PORT', '5000')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port),debug=True)