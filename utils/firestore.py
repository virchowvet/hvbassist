import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Corrige \n duplos escapados para quebra de linha real
raw_json = os.environ["FIREBASE_SERVICE_ACCOUNT_JSON"]
fixed_json = raw_json.replace('\\n', '\n')
service_account_info = json.loads(fixed_json)

cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)
db = firestore.client()
