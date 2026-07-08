import requests
from database import SessionLocal
from models import Station

def import_stations_from_osm():
    """Загружает АЗС из OpenStreetMap через Overpass API"""
    
    print("🔄 Загрузка АЗС из OpenStreetMap...")
    
    # Overpass API запрос
    overpass_query = """[out:json][timeout:120];
area["ISO3166-1"="RU"]->.searchArea;
(
  node["amenity"="fuel"](area.searchArea);
  way["amenity"="fuel"](area.searchArea);
);
out center;"""
    
    url = "https://overpass.kumi.systems/api/interpreter"
    
    try:
        # Используем POST с правильными заголовками
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'AZS-Map/1.0'
        }
        
        response = requests.post(
            url, 
            data={'data': overpass_query},
            headers=headers,
            timeout=120
        )
        response.raise_for_status()
        data = response.json()
        
        print(f"📥 Получено {len(data['elements'])} объектов из OSM")
        
        db = SessionLocal()
        count = 0
        
        for element in data['elements']:
            # Получаем координаты
            if element['type'] == 'node':
                lat = element.get('lat')
                lng = element.get('lon')
            elif element['type'] == 'way':
                center = element.get('center', {})
                lat = center.get('lat')
                lng = center.get('lon')
            else:
                continue
            
            if not lat or not lng:
                continue
            
            # Получаем название
            tags = element.get('tags', {})
            name = tags.get('name', tags.get('brand', 'АЗС'))
            
            brand = tags.get('brand', '')
            if brand:
                name = f"{brand} — {name}" if name != brand else brand
            
            # Проверяем есть ли уже такая АЗС
            existing = db.query(Station).filter(
                abs(Station.lat - lat) < 0.001,
                abs(Station.lng - lng) < 0.001
            ).first()
            
            if existing:
                continue
            
            # Определяем услуги
            amenities = {}
            if tags.get('toilets') == 'yes' or tags.get('amenity') == 'toilets':
                amenities['toilet'] = True
            if tags.get('cafe') == 'yes' or tags.get('amenity') == 'cafe':
                amenities['cafe'] = True
            if tags.get('wifi') == 'yes' or tags.get('internet_access') == 'wlan':
                amenities['wifi'] = True
            if tags.get('shop') == 'convenience':
                amenities['shop'] = True
            
            # Создаём АЗС
            station = Station(
                name=name,
                lat=lat,
                lng=lng,
                amenities=amenities,
                fuels={'92': 'green', '95': 'green', 'dt': 'green'}
            )
            
            db.add(station)
            count += 1
            
            if count % 100 == 0:
                db.commit()
                print(f"✅ Сохранено {count} АЗС...")
        
        db.commit()
        db.close()
        
        print(f"🎉 Импортировано {count} новых АЗС в базу данных!")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка запроса к Overpass API: {e}")
        print(f"   Ответ сервера: {e.response.text if hasattr(e, 'response') else 'N/A'}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    import_stations_from_osm()