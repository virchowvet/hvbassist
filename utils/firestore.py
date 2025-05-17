import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Corrige os caracteres \\n e remove \r e \t residuais
raw_json = os.environ["FIREBASE_SERVICE_ACCOUNT_JSON"]
cleaned_json = raw_json.replace("\\n", "\n").replace("\\r", "").replace("\\t", "")
service_account_info = json.loads(cleaned_json)

# Inicializa o app do Firebase
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)

# Exporta o cliente do Firestore
db = firestore.client()
