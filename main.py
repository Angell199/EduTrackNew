from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="main")

class GradeEntry(BaseModel):
    student_id: str = Field(..., example="2026-001")
    subject_id: str = Field(..., example="SISTEMAS-1")
    activity_name: str = Field(..., example="Examen Parcial I")
    score: float = Field(..., ge=0, le=100, description="La nota debe estar entre 0 y 100")
    recorded_at: Optional[datetime] = datetime.now()

db_repository: List[GradeEntry] = []

@app.post("/api/v1/grades", status_code=201)
async def register_grade(entry: GradeEntry):
    """
    Registra una calificación validando el rango permitido.
    """
    db_repository.append(entry)
    return {
        "status": "success",
        "message": "Calificación registrada correctamente",
        "data": entry
    }

@app.get("/api/v1/grades/{student_id}", response_model=List[GradeEntry])
async def get_academic_history(student_id: str):
    """
    Retorna todos los registros de un estudiante para trazabilidad.
    """
    results = [g for g in db_repository if g.student_id == student_id]
    if not results:
        raise HTTPException(status_code=404, detail="No se encontraron registros para este estudiante")
    return results
