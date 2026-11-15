import os
from fastapi import FastAPI
import psycopg2
import redis

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Sistema Online", "mensagem": "O motor está funcionando!"}

@app.get("/health")
def health_check():
    status = {"api": "ok", "banco_de_dados": "testando...", "cache": "testando..."}
    
    # Testando o Neon (PostgreSQL)
    try:
        db_url = os.environ.get("DATABASE_URL")
        if db_url:
            conn = psycopg2.connect(db_url)
            conn.close()
            status["banco_de_dados"] = "conectado com sucesso"
        else:
            status["banco_de_dados"] = "faltando URL"
    except Exception as e:
        status["banco_de_dados"] = f"erro: {str(e)}"
        
    # Testando o Upstash (Redis)
    try:
        redis_url = os.environ.get("REDIS_URL")
        if redis_url:
            r = redis.from_url(redis_url)
            r.ping()
            status["cache"] = "conectado com sucesso"
        else:
            status["cache"] = "faltando URL"
    except Exception as e:
        status["cache"] = f"erro: {str(e)}"
        
    return status
