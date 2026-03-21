from fastapi import FastAPI, HTTPException
from app import blockchain

app = FastAPI(title="Blockchain File Verification API")


@app.get("/")
def health():
    return {"status": "API running"}


@app.post("/store")
def store_file(content: str):
    try:
        file_hash = blockchain.generate_file_hash(content)
        blockchain.store_hash_on_chain(file_hash)
        return {"hash": file_hash, "stored": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/verify")
def verify_file(content: str):
    try:
        file_hash = blockchain.generate_file_hash(content)
        result = blockchain.verify_hash_on_chain(file_hash)
        return {"hash": file_hash, "verified": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
