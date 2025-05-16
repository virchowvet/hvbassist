from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from openai import OpenAI
import os
import time

from utils.firestore import db
from firebase_admin import firestore

from utils.gpt_processor import processar_texto

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/transcrever")
async def transcrever_audio(
    file: UploadFile,
    paciente: str = Form(...),
    paciente_id: str = Form(...),
    tipo: str = Form("consulta")
):
    try:
        os.makedirs("temp", exist_ok=True)
        filename = f"{paciente_id}_{int(time.time())}.webm"
        audio_path = f"temp/{filename}"

        with open(audio_path, "wb") as f:
            f.write(await file.read())

        with open(audio_path, "rb") as audio_file:
            transcricao = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        texto_transcrito = transcricao.text
        relatorio_html = processar_texto(texto_transcrito, tipo)

        html_path = f"temp/relatorio_{paciente_id}_{int(time.time())}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(relatorio_html)

        db.collection("transcricoes").add({
            "paciente": paciente,
            "paciente_id": paciente_id,
            "tipo": tipo,
            "timestamp": firestore.SERVER_TIMESTAMP,
            "relatorio_html": relatorio_html,
        })

        return JSONResponse(content={
            "status": "ok",
            "html_path": html_path,
            "html": relatorio_html
        })

    except Exception as e:
        print("Erro:", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})