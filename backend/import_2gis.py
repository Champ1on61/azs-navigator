import requests
from database import SessionLocal
from models import Station

# ⚠️ Твой API ключ
API_KEY = 'c99ad782-3c1d-4142-8d7d-ac0a5fec0f15'

def import_2gis_stations():
    """Загружает АЗС из 2GIS API"""
    
    print(" Загрузка АЗС из 2GIS...")
    
    # Координаты центра Москвы + радиус поиска
    cities = [
        {"name": "Москва", "lat": 55.7558, "lng": 37.6173, "radius": 50000},
        {"name": "Санкт-Петербург", "lat": 59.9343, "lng": 30.3351, "radius": 50000},
        {"name": "Казань", "lat": 55.7887, "lng": 49.1221, "radius": 30000},
        {"name": "Екатеринбург", "lat": 56.8389, "lng": 60.6057, "radius": 30000},
        {"name": "Новосибирск", "lat": 55.0084, "lng": 82.9357, "radius": 30000},
    ]
    
    db = SessionLocal()
    total = 0
    
    for city in cities:
        print(f"\n📍 {city['name']}...")
        
        url = "https://catalog.api.2gis.com/3.0/items"
        params = {
            'key': API_KEY,
            'q': 'АЗС',
            'll': f"{city['lng']},{city['lat']}",
            'radius': city['radius'],
            'limit': 500,
            'fields': 'items.point,items.name,items.address_name'
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            items = data.get('result', {}).get('items', [])
            print(f"  📥 Найдено {len(items)} АЗС")
            
            for item in items:
                point = item.get('point', {})
                lat = point.get('lat')
                lng = point.get('lon')
                name = item.get('name', 'АЗС')
                
                if not lat or not lng:
                    continue
                
                existing = db.query(Station).filter(
                    Station.lat.between(lat - 0.0005, lat + 0.0005),
                    Station.lng.between(lng - 0.0005, lng + 0.0005)
                ).first()
                
                if existing:
                    continue
                
                station = Station(
                    name=name,
                    lat=lat,
                    lng=lng,
                    amenities={'toilet': True},
                    fuels={'92': 'green', '95': 'green', 'dt': 'green'}
                )
                db.add(station)
                total += 1
            
            db.commit()
            
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
    
    db.close()
    print(f"\n🏁 Итого: {total} АЗС из 2GIS")

if __name__ == "__main__":
    import_2gis_stations()