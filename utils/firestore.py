import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Corrige os caracteres \\n para \n na chave privada antes de fazer o parse
raw_json = os.environ["FIREBASE_SERVICE_ACCOUNT_JSON"]
fixed_json = raw_json.replace("\\n", "\n")
service_account_info = json.loads(fixed_json)

# Inicializa o app do Firebase
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)

# Exporta o cliente do Firestore
db = firestore.client()
