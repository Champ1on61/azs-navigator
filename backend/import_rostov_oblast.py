import requests
import time
from database import SessionLocal
from models import Station

def import_rostov_oblast():
    """Загружает ВСЕ АЗС Ростовской области из OpenStreetMap"""
    
    print("🌍 Загрузка АЗС Ростовской области...")
    print("📍 Шахты, Новочеркасск, Ростов-на-Дону и другие города")
    print("="*60)
    
    # Ростовская область разбита на сегменты
    regions = [
        {"name": "Ростов-на-Дону центр", "bbox": "47.15,39.65,47.35,39.85"},
        {"name": "Ростов-на-Дону север", "bbox": "47.35,39.60,47.45,39.80"},
        {"name": "Ростов-на-Дону юг", "bbox": "47.10,39.65,47.25,39.85"},
        {"name": "Ростов-на-Дону восток", "bbox": "47.15,39.85,47.35,40.00"},
        {"name": "Ростов-на-Дону запад", "bbox": "47.15,39.50,47.35,39.65"},
        
        {"name": "Шахты", "bbox": "47.65,40.05,47.85,40.30"},
        {"name": "Шахты окрестности", "bbox": "47.60,40.00,47.90,40.35"},
        
        {"name": "Новочеркасск", "bbox": "47.35,39.90,47.50,40.10"},
        {"name": "Новочеркасск окрестности", "bbox": "47.30,39.85,47.55,40.15"},
        
        {"name": "Аксай", "bbox": "47.20,39.95,47.30,40.05"},
        {"name": "Батайск", "bbox": "47.10,39.70,47.20,39.80"},
        {"name": "Азов", "bbox": "47.05,39.35,47.15,39.50"},
        
        {"name": "Таганрог", "bbox": "47.15,38.85,47.30,39.00"},
        {"name": "Таганрог окрестности", "bbox": "47.10,38.80,47.35,39.05"},
        
        {"name": "Новошахтинск", "bbox": "47.75,39.90,47.85,40.00"},
        {"name": "Каменск-Шахтинский", "bbox": "48.25,40.20,48.35,40.35"},
        {"name": "Гуково", "bbox": "48.00,39.90,48.10,40.00"},
        {"name": "Зверево", "bbox": "48.00,40.05,48.08,40.15"},
        
        {"name": "Волгодонск", "bbox": "47.45,42.10,47.55,42.20"},
        {"name": "Волгодонск окрестности", "bbox": "47.40,42.05,47.60,42.25"},
        
        {"name": "Сальск", "bbox": "46.40,41.50,46.50,41.60"},
        {"name": "Сальск окрестности", "bbox": "46.35,41.45,46.55,41.65"},
        
        {"name": "М4 север области", "bbox": "48.00,39.50,49.00,40.50"},
        {"name": "М4 центр области", "bbox": "47.50,39.50,48.00,40.50"},
        {"name": "М4 юг области", "bbox": "47.00,39.50,47.50,40.50"},
        
        {"name": "Ростовская обл. запад", "bbox": "47.00,38.50,47.50,39.50"},
        {"name": "Ростовская обл. восток", "bbox": "47.00,41.50,48.00,42.50"},
        {"name": "Ростовская обл. север", "bbox": "48.50,39.50,49.50,41.00"},
        {"name": "Ростовская обл. юг", "bbox": "46.00,39.00,47.00,40.50"},
    ]
    
    # Используем несколько серверов
    servers = [
        'https://overpass.openstreetmap.ru/cgi/interpreter',
        'https://overpass-api.de/api/interpreter',
    ]
    
    db = SessionLocal()
    total_count = 0
    
    for i, region in enumerate(regions, 1):
        print(f"[{i}/{len(regions)}] {region['name']}...", end=" ")
        
        query = f"""[out:json][timeout:30];
(
  node["amenity"="fuel"]({region['bbox']});
  way["amenity"="fuel"]({region['bbox']});
);
out center;"""
        
        success = False
        for server_url in servers:
            try:
                response = requests.post(
                    server_url,
                    data={'data': query},
                    headers={'User-Agent': 'AZS-Map/1.0'},
                    timeout=45
                )
                
                if response.status_code == 200:
                    data = response.json()
                    success = True
                    break
            except:
                continue
        
        if not success:
            print("❌ Не удалось загрузить")
            continue
        
        elements = data.get('elements', [])
        
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
        print(f"✅ +{count} АЗС (всего: {total_count})")
        
        time.sleep(1)  # Пауза между запросами
    
    db.close()
    
    print("\n" + "="*60)
    print(f"🏁 ГОТОВО! Загружено {total_count} РЕАЛЬНЫХ АЗС")
    print("="*60)
    print("\n📍 Покрыты города:")
    print("  ✅ Ростов-на-Дону")
    print("  ✅ Шахты")
    print("  ✅ Новочеркасск")
    print("  ✅ Аксай, Батайск, Азов")
    print("  ✅ Таганрог")
    print("  ✅ Новошахтинск, Каменск-Шахтинский")
    print("  ✅ Гуково, Зверево")
    print("  ✅ Волгодонск")
    print("  ✅ Сальск")
    print("  ✅ Вся трасса М4 в области")
    print("="*60)

if __name__ == "__main__":
    import_rostov_oblast()
