# backend/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas

router = APIRouter(prefix="/api", tags=["F1 Dashboard"])

# Endpoint pour récupérer toutes les courses
@router.get("/races", response_model=List[schemas.Race])
def read_races(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    races = db.query(models.Race).offset(skip).limit(limit).all()
    return races

# Endpoint pour obtenir la course la plus récente (données live)
@router.get("/live", response_model=schemas.Race)
def get_live_race(db: Session = Depends(get_db)):
    race = db.query(models.Race).order_by(models.Race.date.desc()).first()
    if not race:
        raise HTTPException(status_code=404, detail="Aucune course trouvée")
    return race

# Endpoint de comparaison entre deux pilotes
@router.get("/compare/drivers/{driver1_id}/{driver2_id}", response_model=dict)
def compare_drivers(driver1_id: int, driver2_id: int, db: Session = Depends(get_db)):
    driver1 = db.query(models.Driver).filter(models.Driver.id == driver1_id).first()
    driver2 = db.query(models.Driver).filter(models.Driver.id == driver2_id).first()
    if not driver1 or not driver2:
        raise HTTPException(status_code=404, detail="Pilote non trouvé")
    
    # Exemple de calcul : somme des points obtenus
    driver1_points = sum(result.points for result in driver1.results)
    driver2_points = sum(result.points for result in driver2.results)
    
    return {
        "driver1": {"id": driver1.id, "name": driver1.name, "points": driver1_points},
        "driver2": {"id": driver2.id, "name": driver2.name, "points": driver2_points}
    }
