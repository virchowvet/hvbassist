import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Lê a variável de ambiente que contém o JSON da chave de serviço
service_account_info = json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT_JSON"])

# Inicializa o Firebase com as credenciais da variável
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)

# Cliente Firestore
db = firestore.client()
