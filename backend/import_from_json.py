import requests
from database import SessionLocal
from models import Station

def import_real_stations():
    print("🔄 Загрузка РЕАЛЬНЫХ АЗС из OpenStreetMap...")
    
    # Запрашиваем АЗС вокруг Москвы (пример)
    query = """
    [out:json];
    node["amenity"="fuel"](55.5,37.0,56.0,38.0);
    out;
    """
    
    response = requests.post('https://overpass-api.de/api/interpreter', 
                           data={'data': query})
    data = response.json()
    
    db = SessionLocal()
    count = 0
    
    for item in data['elements']:
        station = Station(
            name=item['tags'].get('name', 'АЗС'),
            lat=item['lat'],
            lng=item['lon'],
            amenities={'toilet': True},  # можно парсить из тегов
            fuels={'92': 'green', '95': 'green', 'dt': 'green'}
        )
        db.add(station)
        count += 1
    
    db.commit()
    db.close()
    print(f"✅ Импортировано {count} РЕАЛЬНЫХ АЗС!")

if __name__ == "__main__":
    import_real_stations()