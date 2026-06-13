from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
import io

from app.pii_detector import detect_pii
from app.masker import mask_value

app = FastAPI(title="PII Detection API")

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/scan")
async def scan(file: UploadFile = File(...)):
    content = await file.read()

    if file.filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(content))
    else:
        return JSONResponse({"error": "Only CSV supported in starter version"}, status_code=400)

    report = []

    for col in df.columns:
        for idx, val in enumerate(df[col]):
            found = detect_pii(str(val))
            for pii_type in found:
                report.append({
                    "row": idx,
                    "column": col,
                    "pii_type": pii_type
                })
                df.at[idx, col] = mask_value(str(val), pii_type)

    output_name = "masked_" + file.filename
    df.to_csv(output_name, index=False)

    return {
        "records_scanned": len(df),
        "pii_found": len(report),
        "masked_file": output_name,
        "report": report[:20]
    }
