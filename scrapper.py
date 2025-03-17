# backend/scraper.py
import requests
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from datetime import datetime

# Création des tables (à n’exécuter qu’une fois)
models.Base.metadata.create_all(bind=engine)

ERGAST_URL = "http://ergast.com/api/f1/current/results.json"

def fetch_and_store_data():
    response = requests.get(ERGAST_URL)
    if response.status_code != 200:
        print("Erreur lors de la récupération des données")
        return
    data = response.json()
    races_data = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])
    
    db: Session = SessionLocal()
    try:
        for race_info in races_data:
            race_date = datetime.strptime(race_info["date"], "%Y-%m-%d")
            # Vérifier si la course existe déjà
            race = db.query(models.Race).filter(models.Race.name == race_info["raceName"]).first()
            if not race:
                race = models.Race(
                    name=race_info["raceName"],
                    date=race_date,
                    circuit=race_info["Circuit"]["circuitName"]
                )
                db.add(race)
                db.commit()
                db.refresh(race)
            
            for result in race_info["Results"]:
                # Traitement du pilote
                driver_info = result["Driver"]
                full_name = f"{driver_info['givenName']} {driver_info['familyName']}"
                driver = db.query(models.Driver).filter(models.Driver.name == full_name).first()
                if not driver:
                    driver = models.Driver(name=full_name, nationality=driver_info["nationality"])
                    db.add(driver)
                    db.commit()
                    db.refresh(driver)
                
                # Traitement de l'écurie (constructeur)
                constructor_info = result["Constructor"]
                team = db.query(models.Team).filter(models.Team.name == constructor_info["name"]).first()
                if not team:
                    team = models.Team(name=constructor_info["name"])
                    db.add(team)
                    db.commit()
                    db.refresh(team)
                
                # Insertion du résultat s'il n'existe pas déjà
                existing_result = db.query(models.Result).filter(
                    models.Result.race_id == race.id,
                    models.Result.driver_id == driver.id
                ).first()
                if not existing_result:
                    new_result = models.Result(
                        race_id=race.id,
                        driver_id=driver.id,
                        team_id=team.id,
                        position=int(result["position"]),
                        points=float(result["points"])
                    )
                    db.add(new_result)
                    db.commit()
    except Exception as e:
        db.rollback()
        print(f"Erreur : {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fetch_and_store_data()
