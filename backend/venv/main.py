from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from datetime import datetime

from database import engine, get_db, Base
from models import Station, ChatMessage, RoadEvent, HelpRequest

Base.metadata.create_all(bind=engine)

app = FastAPI(title='АЗС Карта API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/api/stations')
def get_stations(db: Session = Depends(get_db)):
    stations = db.query(Station).all()
    return stations

@app.get('/api/stations/{station_id}')
def get_station(station_id: int, db: Session = Depends(get_db)):
    station = db.query(Station).filter(Station.id == station_id).first()
    if not station:
        raise HTTPException(status_code=404, detail='АЗС не найдена')
    return station

@app.post('/api/stations/{station_id}/update_status')
def update_station_status(
    station_id: int, 
    fuel_type: str,
    status: str,
    db: Session = Depends(get_db)
):
    station = db.query(Station).filter(Station.id == station_id).first()
    if not station:
        raise HTTPException(status_code=404, detail='АЗС не найдена')
    
    # ВАЖНО: создаём новый dict, а не мутируем старый
    current_fuels = dict(station.fuels) if station.fuels else {}
    current_fuels[fuel_type] = status
    
    station.fuels = current_fuels
    station.updated_at = datetime.utcnow()
    
    # Говорим SQLAlchemy, что поле fuels изменилось
    flag_modified(station, "fuels")
    
    db.commit()
    db.refresh(station)
    
    return {'status': 'ok', 'fuels': station.fuels}

@app.get('/api/stations/{station_id}/chat')
def get_chat(station_id: int, db: Session = Depends(get_db)):
    messages = db.query(ChatMessage).filter(
        ChatMessage.station_id == station_id
    ).order_by(ChatMessage.created_at.desc()).limit(50).all()
    return messages

@app.post('/api/stations/{station_id}/chat')
def send_message(
    station_id: int,
    author_name: str = 'Гость',
    text: str = '',
    db: Session = Depends(get_db)
):
    if len(text) > 500:
        raise HTTPException(status_code=400, detail='Сообщение слишком длинное')
    if not text.strip():
        raise HTTPException(status_code=400, detail='Сообщение пустое')
    message = ChatMessage(
        station_id=station_id,
        author_name=author_name or 'Гость',
        text=text
    )
    db.add(message)
    db.commit()
    return {'status': 'ok', 'message_id': message.id}

@app.get('/api/events')
def get_events(db: Session = Depends(get_db)):
    events = db.query(RoadEvent).filter(RoadEvent.is_active == True).all()
    return events

@app.post('/api/events')
def create_event(
    lat: float,
    lng: float,
    type: str,
    description: str,
    db: Session = Depends(get_db)
):
    event = RoadEvent(lat=lat, lng=lng, type=type, description=description)
    db.add(event)
    db.commit()
    return {'status': 'ok', 'event_id': event.id}

@app.post('/api/help')
def create_help_request(
    lat: float,
    lng: float,
    type: str,
    contact: str,
    comment: str = '',
    db: Session = Depends(get_db)
):
    request = HelpRequest(lat=lat, lng=lng, type=type, contact=contact, comment=comment)
    db.add(request)
    db.commit()
    return {'status': 'ok', 'request_id': request.id}

@app.get('/')
def root():
    return {'message': 'АЗС Карта API работает!', 'docs': '/docs'}