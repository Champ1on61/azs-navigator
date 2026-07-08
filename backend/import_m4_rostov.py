import requests
import time
from database import SessionLocal
from models import Station

def import_m4_rostov_stations():
    """Загружает РЕАЛЬНЫЕ АЗС на трассе М4 в Ростовской области"""
    
    print("🔄 Загрузка АЗС на трассе М4 (Ростовская область)...")
    
    # Bounding boxes вдоль трассы М4 в Ростовской области
    # От границы с Воронежской областью до Ростова-на-Дону и дальше
    segments = [
        {"name": "М4: Шахты - Каменск", "bbox": "48.0,39.5,49.5,41.0"},
        {"name": "М4: Новочеркасск - Шахты", "bbox": "47.2,39.5,48.5,40.5"},
        {"name": "М4: Ростов-на-Дону", "bbox": "47.0,39.3,47.5,40.0"},
        {"name": "М4: Аксай - Ростов", "bbox": "47.1,39.7,47.4,40.2"},
        {"name": "М4: Батайск - Азов", "bbox": "46.9,39.5,47.3,40.0"},
        {"name": "М4: Юг Ростовской обл.", "bbox": "46.5,39.5,47.2,40.5"},
        {"name": "Ростов-на-Дону город", "bbox": "47.15,39.6,47.35,39.9"},
        {"name": "Шахты город", "bbox": "47.6,40.0,47.8,40.3"},
        {"name": "Новочеркасск", "bbox": "47.35,39.85,47.5,40.1"},
        {"name": "Таганрог", "bbox": "47.15,38.8,47.3,39.1"},
        {"name": "Волгодонск", "bbox": "47.45,42.0,47.65,42.3"},
        {"name": "Сальск", "bbox": "46.4,41.4,46.6,41.7"},
        {"name": "Зверево - Гуково", "bbox": "48.0,39.8,48.3,40.2"},
    ]
    
    db = SessionLocal()
    total_count = 0
    
    for segment in segments:
        print(f"\n📍 {segment['name']}...")
        
        query = f"""[out:json][timeout:60];
(
  node["amenity"="fuel"]({segment['bbox']});
  way["amenity"="fuel"]({segment['bbox']});
);
out center;"""
        
        try:
            response = requests.post(
    'https://overpass-api.de/api/interpreter',
                data={'data': query},
                headers={'User-Agent': 'AZS-Map/1.0'},
                timeout=90
            )
            response.raise_for_status()
            data = response.json()
            
            elements = data.get('elements', [])
            print(f"  📥 Найдено {len(elements)} объектов")
            
            count = 0
            for element in elements:
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
                
                tags = element.get('tags', {})
                
                # Получаем название
                name = tags.get('name', '')
                brand = tags.get('brand', '')
                operator = tags.get('operator', '')
                
                if not name and brand:
                    name = brand
                elif not name and operator:
                    name = operator
                elif not name:
                    name = 'АЗС'
                
                # Добавляем бренд к названию если есть
                if brand and brand.lower() not in name.lower():
                    name = f"{brand} — {name}"
                
                # Проверяем дубликаты (точность 0.001 ≈ 100 метров)
                existing = db.query(Station).filter(
                    Station.lat.between(lat - 0.001, lat + 0.001),
                    Station.lng.between(lng - 0.001, lng + 0.001)
                ).first()
                
                if existing:
                    continue
                
                # Парсим услуги из тегов OSM
                amenities = {}
                if tags.get('toilets') == 'yes':
                    amenities['toilet'] = True
                if tags.get('cafe') == 'yes' or tags.get('amenity') == 'cafe':
                    amenities['cafe'] = True
                if tags.get('internet_access') == 'wlan' or tags.get('wifi') == 'yes':
                    amenities['wifi'] = True
                if tags.get('shop') == 'convenience':
                    amenities['shop'] = True
                if tags.get('fuel:diesel') == 'yes':
                    pass  # есть дизель
                if tags.get('car_wash') == 'yes':
                    amenities['car_wash'] = True
                
                station = Station(
                    name=name,
                    lat=lat,
                    lng=lng,
                    amenities=amenities,
                    fuels={'92': 'green', '95': 'green', 'dt': 'green'}
                )
                
                db.add(station)
                count += 1
                
                if count % 20 == 0:
                    db.commit()
                    print(f"  ✅ Сохранено {count}...")
            
            db.commit()
            total_count += count
            print(f"  🎉 Добавлено {count} АЗС")
            
            time.sleep(2)  # пауза чтобы не перегружать сервер
            
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
            continue
    
    db.close()
    print(f"\n{'='*50}")
    print(f"🏁 ИТОГО импортировано {total_count} РЕАЛЬНЫХ АЗС на М4!")
    print(f"{'='*50}")

if __name__ == "__main__":
    import_m4_rostov_stations()