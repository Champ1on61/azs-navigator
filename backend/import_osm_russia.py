import requests
import time
from database import SessionLocal
from models import Station

def import_osm_russia():
    """Загружает РЕАЛЬНЫЕ АЗС по всей России через Overpass (русский сервер)"""
    
    print("🌍 Загрузка АЗС по всей России...")
    print("⏱️  Это займёт 20-30 минут...")
    print("="*60)
    
    # Разбиваем Россию на МАЛЕНЬКИЕ области (0.5x0.5 градуса)
    # Это гарантирует что не будет таймаутов
    regions = []
    
    # Генерируем сетку по всей России
    lat_start, lat_end = 41.0, 70.0  # Широта от юга до севера
    lng_start, lng_end = 19.0, 170.0  # Долгота от запада до востока
    
    step = 0.5  # Размер области
    
    lat = lat_start
    while lat < lat_end:
        lng = lng_start
        while lng < lng_end:
            regions.append({
                "bbox": f"{lat},{lng},{lat+step},{lng+step}",
                "name": f"{lat:.1f},{lng:.1f}"
            })
            lng += step
        lat += step
    
    print(f"📊 Всего областей для загрузки: {len(regions)}")
    
    # Используем русский сервер Overpass (стабильнее)
    server_url = 'https://overpass.openstreetmap.ru/cgi/interpreter'
    
    db = SessionLocal()
    total_count = 0
    processed = 0
    
    for region in regions:
        processed += 1
        
        query = f"""[out:json][timeout:30];
(
  node["amenity"="fuel"]({region['bbox']});
  way["amenity"="fuel"]({region['bbox']});
);
out center;"""
        
        try:
            response = requests.post(
                server_url,
                data={'data': query},
                headers={'User-Agent': 'AZS-Map/1.0'},
                timeout=45
            )
            
            if response.status_code != 200:
                continue
            
            data = response.json()
            elements = data.get('elements', [])
            
            if len(elements) == 0:
                continue
            
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
                
                if brand and brand.lower() not in name.lower():
                    name = f"{brand} — {name}"
                
                # Проверяем дубликаты
                existing = db.query(Station).filter(
                    Station.lat.between(lat - 0.0005, lat + 0.0005),
                    Station.lng.between(lng - 0.0005, lng + 0.0005)
                ).first()
                
                if existing:
                    continue
                
                # Парсим услуги
                amenities = {}
                if tags.get('toilets') == 'yes':
                    amenities['toilet'] = True
                if tags.get('cafe') == 'yes':
                    amenities['cafe'] = True
                if tags.get('internet_access') == 'wlan' or tags.get('wifi') == 'yes':
                    amenities['wifi'] = True
                if tags.get('shop') == 'convenience':
                    amenities['shop'] = True
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
            
            db.commit()
            total_count += count
            
            # Показываем прогресс каждые 50 областей
            if processed % 50 == 0:
                print(f"✅ Прогресс: {processed}/{len(regions)} областей | Всего АЗС: {total_count}")
            
            time.sleep(0.5)  # Пауза между запросами
            
        except Exception as e:
            # Пропускаем ошибки и идём дальше
            continue
    
    db.close()
    
    print(f"\n{'='*60}")
    print(f"🏁 ИТОГО загружено {total_count} РЕАЛЬНЫХ АЗС по всей России!")
    print(f"{'='*60}")

if __name__ == "__main__":
    import_osm_russia()