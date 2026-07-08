import requests
import time
from database import SessionLocal
from models import Station

def import_all_russia_stations():
    """Загружает ВСЕ РЕАЛЬНЫЕ АЗС по всей России из OpenStreetMap"""
    
    print("🌍 Загрузка ВСЕХ АЗС по России...")
    print("⏱️  Это займёт 15-20 минут...")
    
    # Разбиваем Россию на мелкие регионы (чтобы не было таймаутов)
    regions = [
        # Центральный федеральный округ
        {"name": "Москва", "bbox": "55.5,37.0,56.0,38.0"},
        {"name": "Московская обл. север", "bbox": "56.0,36.0,57.0,39.0"},
        {"name": "Московская обл. юг", "bbox": "54.5,36.0,55.5,39.0"},
        {"name": "Тула", "bbox": "53.8,37.0,54.5,38.5"},
        {"name": "Калуга", "bbox": "53.5,34.5,54.5,36.5"},
        {"name": "Рязань", "bbox": "54.0,39.0,55.0,40.5"},
        {"name": "Владимир", "bbox": "55.8,39.5,56.8,41.0"},
        {"name": "Ярославль", "bbox": "57.0,39.0,58.5,40.5"},
        {"name": "Кострома", "bbox": "57.5,40.5,58.5,42.0"},
        {"name": "Иваново", "bbox": "56.5,40.5,57.5,42.0"},
        {"name": "Тверь", "bbox": "56.0,34.5,57.5,36.5"},
        {"name": "Смоленск", "bbox": "54.0,31.5,55.5,33.5"},
        {"name": "Брянск", "bbox": "52.5,32.5,53.5,34.5"},
        {"name": "Орёл", "bbox": "52.5,35.5,53.5,37.0"},
        {"name": "Курск", "bbox": "51.0,35.5,52.5,37.5"},
        {"name": "Белгород", "bbox": "50.0,36.0,51.5,38.0"},
        {"name": "Воронеж", "bbox": "51.0,38.5,52.5,40.5"},
        {"name": "Липецк", "bbox": "52.0,39.0,53.5,40.5"},
        {"name": "Тамбов", "bbox": "52.0,41.0,53.5,42.5"},
        
        # Северо-Западный федеральный округ
        {"name": "Санкт-Петербург", "bbox": "59.5,29.5,60.5,31.0"},
        {"name": "Ленинградская обл.", "bbox": "59.0,28.0,61.0,34.0"},
        {"name": "Новгород", "bbox": "57.5,30.5,59.0,33.0"},
        {"name": "Псков", "bbox": "56.5,27.5,58.5,30.5"},
        {"name": "Калининград", "bbox": "54.5,19.5,55.5,21.5"},
        {"name": "Мурманск", "bbox": "67.5,32.5,69.0,34.5"},
        {"name": "Архангельск", "bbox": "63.5,39.5,65.5,42.0"},
        {"name": "Вологда", "bbox": "59.0,38.5,60.5,40.5"},
        {"name": "Карелия", "bbox": "61.0,33.0,64.0,36.0"},
        {"name": "Коми", "bbox": "63.0,49.0,66.0,53.0"},
        
        # Южный федеральный округ
        {"name": "Ростов-на-Дону", "bbox": "47.0,39.3,47.5,40.0"},
        {"name": "Ростовская обл. север", "bbox": "48.0,39.0,49.5,41.5"},
        {"name": "Ростовская обл. юг", "bbox": "46.0,39.0,47.5,41.5"},
        {"name": "Краснодар", "bbox": "44.8,38.8,45.3,39.3"},
        {"name": "Краснодарский край север", "bbox": "45.5,38.5,46.5,40.5"},
        {"name": "Краснодарский край юг", "bbox": "43.5,39.5,44.5,41.0"},
        {"name": "Адыгея", "bbox": "44.5,39.5,45.0,40.5"},
        {"name": "Крым", "bbox": "44.3,33.5,45.5,35.5"},
        {"name": "Севастополь", "bbox": "44.3,33.3,44.7,33.7"},
        {"name": "Волгоград", "bbox": "48.5,44.0,49.0,44.8"},
        {"name": "Волгоградская обл.", "bbox": "49.0,43.0,50.5,45.5"},
        {"name": "Астрахань", "bbox": "46.0,47.5,47.0,48.5"},
        
        # Северо-Кавказский федеральный округ
        {"name": "Ставрополь", "bbox": "45.0,41.5,45.5,42.5"},
        {"name": "Ставропольский край", "bbox": "44.0,41.0,46.0,44.0"},
        {"name": "Дагестан", "bbox": "42.0,46.5,43.5,48.5"},
        {"name": "Чечня", "bbox": "43.0,45.5,44.0,46.5"},
        {"name": "Ингушетия", "bbox": "43.0,44.5,43.5,45.5"},
        {"name": "Северная Осетия", "bbox": "42.5,43.5,43.5,44.5"},
        {"name": "Кабардино-Балкария", "bbox": "43.0,43.0,44.0,44.0"},
        {"name": "Карачаево-Черкесия", "bbox": "43.5,41.5,44.5,42.5"},
        
        # Поволжье
        {"name": "Нижний Новгород", "bbox": "56.0,43.5,56.5,44.5"},
        {"name": "Нижегородская обл.", "bbox": "55.5,42.0,57.5,45.5"},
        {"name": "Казань", "bbox": "55.7,48.8,55.9,49.3"},
        {"name": "Татарстан", "bbox": "54.5,48.0,56.5,51.0"},
        {"name": "Самара", "bbox": "53.0,49.8,53.5,50.5"},
        {"name": "Самарская обл.", "bbox": "52.0,49.0,54.5,52.0"},
        {"name": "Саратов", "bbox": "51.3,45.8,51.8,46.3"},
        {"name": "Саратовская обл.", "bbox": "50.5,44.0,52.5,47.5"},
        {"name": "Пенза", "bbox": "53.0,44.8,53.5,45.5"},
        {"name": "Ульяновск", "bbox": "54.0,48.0,54.5,48.8"},
        {"name": "Удмуртия", "bbox": "56.5,52.0,58.0,54.0"},
        {"name": "Марий Эл", "bbox": "56.5,47.5,57.5,49.0"},
        {"name": "Чувашия", "bbox": "55.0,46.5,56.0,48.0"},
        {"name": "Мордовия", "bbox": "54.0,43.5,55.0,45.5"},
        {"name": "Башкортостан", "bbox": "53.5,54.0,55.5,57.5"},
        {"name": "Оренбург", "bbox": "51.5,54.8,52.0,55.5"},
        
        # Урал
        {"name": "Екатеринбург", "bbox": "56.7,60.4,57.0,60.8"},
        {"name": "Свердловская обл.", "bbox": "56.0,59.0,58.5,62.0"},
        {"name": "Челябинск", "bbox": "55.0,61.2,55.3,61.6"},
        {"name": "Челябинская обл.", "bbox": "54.0,60.0,56.0,63.0"},
        {"name": "Курган", "bbox": "55.3,65.0,55.7,65.5"},
        {"name": "Тюмень", "bbox": "57.0,65.3,57.3,65.8"},
        {"name": "Тюменская обл.", "bbox": "56.0,64.0,58.5,67.0"},
        {"name": "Ханты-Мансийск", "bbox": "60.8,68.8,61.3,69.5"},
        {"name": "Ямало-Ненецкий АО", "bbox": "63.0,66.0,67.0,72.0"},
        {"name": "Пермь", "bbox": "57.8,56.0,58.2,56.5"},
        {"name": "Пермский край", "bbox": "57.0,54.5,59.5,58.0"},
        
        # Сибирь
        {"name": "Новосибирск", "bbox": "54.9,82.8,55.1,83.1"},
        {"name": "Новосибирская обл.", "bbox": "54.0,81.0,56.5,84.5"},
        {"name": "Омск", "bbox": "54.9,73.3,55.1,73.5"},
        {"name": "Омская обл.", "bbox": "54.0,72.0,56.5,75.0"},
        {"name": "Томск", "bbox": "56.3,84.8,56.6,85.2"},
        {"name": "Томская обл.", "bbox": "56.0,83.0,58.5,87.0"},
        {"name": "Кемерово", "bbox": "55.3,86.0,55.5,86.3"},
        {"name": "Кемеровская обл.", "bbox": "54.0,85.0,56.5,88.0"},
        {"name": "Алтайский край", "bbox": "52.0,82.0,54.0,85.0"},
        {"name": "Республика Алтай", "bbox": "50.0,86.0,52.0,88.0"},
        {"name": "Красноярск", "bbox": "55.9,92.7,56.1,93.0"},
        {"name": "Красноярский край", "bbox": "54.0,90.0,58.0,96.0"},
        {"name": "Иркутск", "bbox": "52.2,104.2,52.4,104.4"},
        {"name": "Иркутская обл.", "bbox": "51.0,102.0,54.0,106.0"},
        {"name": "Бурятия", "bbox": "51.0,106.0,53.0,109.0"},
        {"name": "Забайкальский край", "bbox": "51.0,113.0,53.5,118.0"},
        {"name": "Тыва", "bbox": "50.5,93.0,52.5,96.0"},
        {"name": "Хакасия", "bbox": "53.0,89.0,54.5,91.0"},
        
        # Дальний Восток
        {"name": "Якутск", "bbox": "61.9,129.6,62.1,129.9"},
        {"name": "Саха (Якутия)", "bbox": "60.0,125.0,64.0,132.0"},
        {"name": "Хабаровск", "bbox": "48.4,135.0,48.6,135.2"},
        {"name": "Хабаровский край", "bbox": "47.5,133.0,50.0,137.0"},
        {"name": "Владивосток", "bbox": "43.1,131.8,43.2,132.0"},
        {"name": "Приморский край", "bbox": "42.5,131.0,44.5,134.0"},
        {"name": "Амурская обл.", "bbox": "49.0,127.0,51.0,130.0"},
        {"name": "Еврейская АО", "bbox": "48.3,132.0,48.7,132.8"},
        {"name": "Магадан", "bbox": "59.5,150.7,59.7,151.0"},
        {"name": "Камчатка", "bbox": "53.0,158.5,53.3,158.9"},
        {"name": "Сахалин", "bbox": "46.8,142.6,47.1,143.0"},
        {"name": "Чукотка", "bbox": "64.5,170.0,65.0,171.0"},
    ]
    
    # Несколько серверов Overpass (если один не работает, пробуем другой)
    servers = [
        'https://overpass-api.de/api/interpreter',
        'https://overpass.kumi.systems/api/interpreter',
        'https://overpass.openstreetmap.ru/api/interpreter',
    ]
    
    db = SessionLocal()
    total_count = 0
    failed_regions = []
    
    for region in regions:
        print(f"\n📍 {region['name']}...")
        
        query = f"""[out:json][timeout:60];
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
                    timeout=90
                )
                response.raise_for_status()
                data = response.json()
                success = True
                break
            except Exception as e:
                print(f"  ⚠️  Сервер {server_url} не ответил: {type(e).__name__}")
                continue
        
        if not success:
            print(f"  ❌ Все серверы недоступны, пропускаем")
            failed_regions.append(region['name'])
            continue
        
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
            
            if count % 20 == 0:
                db.commit()
        
        db.commit()
        total_count += count
        print(f"  ✅ Добавлено {count} АЗС")
        
        time.sleep(1)  # Пауза между запросами
    
    db.close()
    
    print(f"\n{'='*60}")
    print(f"🏁 ИТОГО загружено {total_count} РЕАЛЬНЫХ АЗС по всей России!")
    print(f"{'='*60}")
    
    if failed_regions:
        print(f"\n⚠️  Не удалось загрузить регионы:")
        for r in failed_regions:
            print(f"  - {r}")

if __name__ == "__main__":
    import_all_russia_stations()