import requests
import time
from database import SessionLocal
from models import Station

def import_real_stations():
    print("🔄 Загрузка РЕАЛЬНЫХ АЗС из OpenStreetMap...")
    
    regions = [
        {"name": "Москва и МО", "bbox": "54.5,35.0,56.5,39.0"},
        {"name": "Санкт-Петербург", "bbox": "59.0,28.0,61.0,32.0"},
        {"name": "Центр", "bbox": "52.0,32.0,56.0,42.0"},
    ]
    
    db = SessionLocal()
    total = 0
    
    for region in regions:
        print(f"\n📍 {region['name']}...")
        
        query = f"""[out:json][timeout:90];
(
  node["amenity"="fuel"]({region['bbox']});
  way["amenity"="fuel"]({region['bbox']});
);
out center;"""
        
        try:
            response = requests.post(
                'https://overpass.kumi.systems/api/interpreter',
                data={'data': query},
                headers={'User-Agent': 'AZS-Map/1.0'},
                timeout=120
            )
            data = response.json()
            
            count = 0
            for element in data['elements']:
                if element['type'] == 'node':
                    lat, lng = element.get('lat'), element.get('lon')
                elif element['type'] == 'way':
                    center = element.get('center', {})
                    lat, lng = center.get('lat'), center.get('lon')
                else:
                    continue
                
                if not lat or not lng:
                    continue
                
                tags = element.get('tags', {})
                name = tags.get('name', tags.get('brand', 'АЗС'))
                
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
                count += 1
            
            db.commit()
            total += count
            print(f"  ✅ Добавлено {count} АЗС")
            time.sleep(2)
            
        except Exception as e:
            print(f"   Ошибка: {e}")
    
    db.close()
    print(f"\n🏁 Итого: {total} РЕАЛЬНЫХ АЗС!")

if __name__ == "__main__":
    import_real_stations()