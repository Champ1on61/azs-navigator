import requests
from database import SessionLocal
from models import Station

# Твой API ключ 2GIS
API_KEY = 'c99ad782-3c1d-4142-8d7d-ac0a5fec0f15'

def import_2gis_stations():
    """Загружает РЕАЛЬНЫЕ АЗС из 2GIS по всей России"""
    
    print("🌍 Загрузка АЗС из 2GIS по всей России...")
    print("🔑 Используем API ключ...")
    
    # Крупные города России с радиусом поиска
    cities = [
        # Центральный ФО
        {"name": "Москва", "lat": 55.7558, "lng": 37.6173, "radius": 50000},
        {"name": "Воронеж", "lat": 51.6720, "lng": 39.1843, "radius": 30000},
        {"name": "Тула", "lat": 54.1961, "lng": 37.6182, "radius": 25000},
        {"name": "Рязань", "lat": 54.6269, "lng": 39.6916, "radius": 25000},
        {"name": "Ярославль", "lat": 57.6261, "lng": 39.8845, "radius": 25000},
        {"name": "Тверь", "lat": 56.8587, "lng": 35.9176, "radius": 25000},
        {"name": "Калуга", "lat": 54.5293, "lng": 36.2754, "radius": 25000},
        {"name": "Белгород", "lat": 50.5977, "lng": 36.5870, "radius": 25000},
        {"name": "Курск", "lat": 51.7303, "lng": 36.1927, "radius": 25000},
        {"name": "Брянск", "lat": 53.2434, "lng": 34.3656, "radius": 25000},
        {"name": "Орёл", "lat": 52.9735, "lng": 36.0535, "radius": 25000},
        {"name": "Липецк", "lat": 52.6031, "lng": 39.5708, "radius": 25000},
        {"name": "Тамбов", "lat": 52.7213, "lng": 41.4520, "radius": 25000},
        
        # Северо-Западный ФО
        {"name": "Санкт-Петербург", "lat": 59.9343, "lng": 30.3351, "radius": 50000},
        {"name": "Калининград", "lat": 54.7104, "lng": 20.4522, "radius": 30000},
        {"name": "Мурманск", "lat": 68.9700, "lng": 33.0900, "radius": 25000},
        {"name": "Архангельск", "lat": 64.5393, "lng": 40.5328, "radius": 25000},
        {"name": "Вологда", "lat": 59.2239, "lng": 39.8839, "radius": 25000},
        {"name": "Псков", "lat": 57.8136, "lng": 28.3496, "radius": 25000},
        {"name": "Великий Новгород", "lat": 58.5218, "lng": 31.2758, "radius": 25000},
        
        # Южный ФО
        {"name": "Ростов-на-Дону", "lat": 47.2357, "lng": 39.7015, "radius": 50000},
        {"name": "Краснодар", "lat": 45.0355, "lng": 38.9753, "radius": 40000},
        {"name": "Волгоград", "lat": 48.7080, "lng": 44.5133, "radius": 35000},
        {"name": "Астрахань", "lat": 46.3497, "lng": 48.0408, "radius": 30000},
        {"name": "Сочи", "lat": 43.6028, "lng": 39.7342, "radius": 30000},
        {"name": "Симферополь", "lat": 44.9521, "lng": 34.1024, "radius": 30000},
        {"name": "Севастополь", "lat": 44.6167, "lng": 33.5254, "radius": 25000},
        {"name": "Новороссийск", "lat": 44.7230, "lng": 37.7696, "radius": 25000},
        
        # Северо-Кавказский ФО
        {"name": "Ставрополь", "lat": 45.0428, "lng": 41.9734, "radius": 30000},
        {"name": "Махачкала", "lat": 42.9849, "lng": 47.5047, "radius": 25000},
        {"name": "Грозный", "lat": 43.3181, "lng": 45.6986, "radius": 25000},
        {"name": "Владикавказ", "lat": 43.0370, "lng": 44.6680, "radius": 20000},
        {"name": "Нальчик", "lat": 43.4981, "lng": 43.6189, "radius": 20000},
        
        # Приволжский ФО
        {"name": "Нижний Новгород", "lat": 56.3269, "lng": 44.0059, "radius": 40000},
        {"name": "Казань", "lat": 55.7887, "lng": 49.1221, "radius": 40000},
        {"name": "Самара", "lat": 53.2001, "lng": 50.1500, "radius": 35000},
        {"name": "Саратов", "lat": 51.5336, "lng": 46.0342, "radius": 30000},
        {"name": "Уфа", "lat": 54.7388, "lng": 55.9721, "radius": 35000},
        {"name": "Пермь", "lat": 58.0105, "lng": 56.2502, "radius": 30000},
        {"name": "Оренбург", "lat": 51.7683, "lng": 55.0964, "radius": 30000},
        {"name": "Ульяновск", "lat": 54.3142, "lng": 48.4031, "radius": 25000},
        {"name": "Пенза", "lat": 53.2001, "lng": 45.0000, "radius": 25000},
        {"name": "Тольятти", "lat": 53.5303, "lng": 49.3461, "radius": 25000},
        {"name": "Ижевск", "lat": 56.8527, "lng": 53.2041, "radius": 25000},
        
        # Уральский ФО
        {"name": "Екатеринбург", "lat": 56.8389, "lng": 60.6057, "radius": 40000},
        {"name": "Челябинск", "lat": 55.1644, "lng": 61.4368, "radius": 35000},
        {"name": "Тюмень", "lat": 57.1522, "lng": 65.5272, "radius": 30000},
        {"name": "Курган", "lat": 55.4500, "lng": 65.3333, "radius": 25000},
        {"name": "Сургут", "lat": 61.2500, "lng": 73.4167, "radius": 25000},
        {"name": "Нижневартовск", "lat": 60.9344, "lng": 76.5531, "radius": 25000},
        
        # Сибирский ФО
        {"name": "Новосибирск", "lat": 55.0084, "lng": 82.9357, "radius": 40000},
        {"name": "Омск", "lat": 54.9885, "lng": 73.3242, "radius": 35000},
        {"name": "Красноярск", "lat": 56.0153, "lng": 92.8932, "radius": 35000},
        {"name": "Иркутск", "lat": 52.2870, "lng": 104.3050, "radius": 30000},
        {"name": "Барнаул", "lat": 53.3606, "lng": 83.7636, "radius": 30000},
        {"name": "Кемерово", "lat": 55.3333, "lng": 86.0833, "radius": 25000},
        {"name": "Томск", "lat": 56.4977, "lng": 84.9744, "radius": 25000},
        {"name": "Новокузнецк", "lat": 53.7596, "lng": 87.1264, "radius": 25000},
        
        # Дальневосточный ФО
        {"name": "Владивосток", "lat": 43.1198, "lng": 131.8869, "radius": 30000},
        {"name": "Хабаровск", "lat": 48.4827, "lng": 135.0848, "radius": 30000},
        {"name": "Благовещенск", "lat": 50.2667, "lng": 127.5333, "radius": 25000},
        {"name": "Южно-Сахалинск", "lat": 46.9588, "lng": 142.7387, "radius": 25000},
        {"name": "Петропавловск-Камчатский", "lat": 53.0446, "lng": 158.6500, "radius": 25000},
        {"name": "Якутск", "lat": 62.0397, "lng": 129.7317, "radius": 25000},
    ]
    
    db = SessionLocal()
    total_count = 0
    failed_cities = []
    
    for city in cities:
        print(f"\n📍 {city['name']}...")
        
        url = "https://catalog.api.2gis.com/3.0/items"
        params = {
            'key': API_KEY,
            'q': 'АЗС',
            'll': f"{city['lng']},{city['lat']}",
            'radius': city['radius'],
            'limit': 500,
            'fields': 'items.point,items.name,items.address_name,items.floors'
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            if response.status_code != 200:
                print(f"  ❌ Ошибка API: {data.get('error_message', 'Unknown error')}")
                failed_cities.append(city['name'])
                continue
            
            items = data.get('result', {}).get('items', [])
            print(f"  📥 Найдено {len(items)} АЗС")
            
            count = 0
            for item in items:
                point = item.get('point', {})
                lat = point.get('lat')
                lng = point.get('lon')
                name = item.get('name', 'АЗС')
                
                if not lat or not lng:
                    continue
                
                # Проверяем дубликаты
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
                    amenities={'toilet': True},  # Можно расширить парсинг
                    fuels={'92': 'green', '95': 'green', 'dt': 'green'}
                )
                db.add(station)
                count += 1
            
            db.commit()
            total_count += count
            print(f"  ✅ Добавлено {count} АЗС")
            
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
            failed_cities.append(city['name'])
            continue
    
    db.close()
    
    print(f"\n{'='*60}")
    print(f"🏁 ИТОГО загружено {total_count} РЕАЛЬНЫХ АЗС из 2GIS!")
    print(f"{'='*60}")
    
    if failed_cities:
        print(f"\n⚠️  Не удалось загрузить {len(failed_cities)} городов:")
        for c in failed_cities[:10]:  # Показываем первые 10
            print(f"  - {c}")
        if len(failed_cities) > 10:
            print(f"  ... и ещё {len(failed_cities) - 10}")

if __name__ == "__main__":
    import_2gis_stations()
    