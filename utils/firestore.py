import firebase_admin
from firebase_admin import credentials, firestore

# Substitua pelo caminho real da sua chave quando fizer o download
cred = credentials.Certificate("utils/firebase_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()