from fastapi import FastAPI, Depends
from model import get_db
from datetime import datetime, timedelta
from pydantic import BaseModel

class SessionComplete(BaseModel):
    duration_minutes: int

app = FastAPI()

# GET /api/v1/dashboard
@app.get("/api/v1/dashboard", status_code = 200)
async def dashboard(db = Depends(get_db)):
    data = db.execute(
        """
        SELECT streak, total_sessions FROM stats
        """
    ).fetchone()

    plants = db.execute(
        """
        SELECT * FROM plants
        WHERE completed = 0
        ORDER BY id 
        LIMIT 1
        """
    ).fetchone()

    context = {
        "streak": data["streak"],
        "total_sessions": data["total_sessions"],
        "plants": plants
    }

    return context

# POST /api/v1/complete_session
@app.post("/api/v1/complete_session", status_code = 201)
async def complete_session(data: SessionComplete, db = Depends(get_db)):
    now = datetime.utcnow()
    one_day = timedelta(days = 1)

    duration_minutes = data.duration_minutes

    streak = 0

    # Add session
    db.execute(
        """
        INSERT INTO sessions(completed_at, duration_minutes)
        VALUES(?, ?)
        """,
        (now.isoformat(), duration_minutes)
    )

    # Update stats table
    stats = db.execute(
        """
        SELECT * FROM stats
        """
    ).fetchone()

    # first-time user
    if stats["total_sessions"] == 0:
        streak = 1
    else:
        if now.date() - datetime.fromisoformat(stats["last_completed_date"]).date() == one_day:
            streak = stats["streak"] + 1
        else:
            streak = 1
    
    db.execute(
        """
        UPDATE stats 
        SET streak = ?, total_sessions = ?, last_completed_date = ?
        """,
        (streak, stats["total_sessions"] + 1, now.isoformat())
    )

    # Retrieving plant info 
    current_plant = db.execute(
        """
        SELECT * FROM plants
        WHERE completed = ? 
        ORDER BY id
        LIMIT 1
        """,
        (0,)
    ).fetchone()

    new_sess_completed = current_plant["sessions_completed"] + 1

    # Updating plant
    db.execute(
        """
        UPDATE plants
        SET sessions_completed = ?, completed = ?
        WHERE id = ?
        """,
        (new_sess_completed, 
        new_sess_completed == current_plant["sessions_required"], 
        current_plant["id"])
    )

    # Retrieve updated plant info
    new_plant = db.execute(
        """
        SELECT * FROM plants
        WHERE id = ?
        """,
        (current_plant["id"],)
    ).fetchone()

    context = {
        "streak": streak,
        "total_sessions": stats["total_sessions"] + 1,
        "plant": new_plant
    }

    return context