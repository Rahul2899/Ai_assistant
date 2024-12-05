from fastapi import FastAPI
from pydantic import BaseModel
from system_overview import get_system_overview
from incident_resolution import resolve_incident
from documentation import document_incident

app = FastAPI()

class Issue(BaseModel):
    description: str

@app.get("/system-overview")
def system_overview():
    return {"overview": get_system_overview()}

@app.post("/resolve-incident")
def resolve_incident_endpoint(issue: Issue):
    resolution = resolve_incident(issue.description)
    return {"resolution": resolution}

@app.post("/document-incident")
def document_incident_endpoint(issue: Issue, resolution: str):
    document_incident(issue.description, resolution)
    return {"message": "Incident documented successfully"}