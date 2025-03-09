from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from data.clinicianData import clinicians
from data.clientData import clients
from generateSchedule import generate_schedules

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ClinicianIDRequest(BaseModel):
    clinician_id: str

@app.get("/")
async def health_check():
    return {"status": "healthy"}

@app.post("/generate-schedules")
def generate_schedules_endpoint(request: ClinicianIDRequest):
    clinician_id = request.clinician_id
    
    clinician = next((c for c in clinicians if c["id"] == clinician_id), None)
    if not clinician:
        raise HTTPException(status_code=404, detail="Clinician not found")


    schedules = generate_schedules(clinician, clients)

    return {"schedules": schedules}
 
     