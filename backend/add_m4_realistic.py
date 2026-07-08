from database import SessionLocal
from models import Station

def add_m4_realistic_stations():
    print("🔄 Добавление АЗС на М4 (Ростовская область)...")
    
    stations_data = [
        {"name": "Лукойл, М4 935 км", "lat": 47.7089, "lng": 40.2147, "amenities": {"toilet": True, "cafe": True, "wifi": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Газпромнефть, Шахты", "lat": 47.7234, "lng": 40.2456, "amenities": {"toilet": True, "shower": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Роснефть, М4 940 км", "lat": 47.6891, "lng": 40.1923, "amenities": {"toilet": True, "cafe": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Татнефть, Шахты", "lat": 47.7156, "lng": 40.2289, "amenities": {"toilet": True, "wifi": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Лукойл, Новочеркасск", "lat": 47.4234, "lng": 40.0956, "amenities": {"toilet": True, "cafe": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Газпромнефть, М4 1020 км", "lat": 47.4089, "lng": 40.0734, "amenities": {"toilet": True, "shower": True, "wifi": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Роснефть, Новочеркасск", "lat": 47.4312, "lng": 40.1123, "amenities": {"toilet": True, "cafe": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Лукойл, Аксай", "lat": 47.2689, "lng": 39.9956, "amenities": {"toilet": True, "cafe": True, "wifi": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Газпромнефть, М4 1070 км", "lat": 47.2534, "lng": 39.9823, "amenities": {"toilet": True, "shower": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Shell, Аксай", "lat": 47.2712, "lng": 39.9912, "amenities": {"toilet": True, "cafe": True, "wifi": True, "atm": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Лукойл, Ростов", "lat": 47.2357, "lng": 39.7015, "amenities": {"toilet": True, "cafe": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Газпромнефть, Ростов", "lat": 47.2289, "lng": 39.6934, "amenities": {"toilet": True, "shower": True, "wifi": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Роснефть, Ростов", "lat": 47.2412, "lng": 39.7123, "amenities": {"toilet": True, "cafe": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "BP, Ростов", "lat": 47.2178, "lng": 39.6856, "amenities": {"toilet": True, "cafe": True, "wifi": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Shell, Ростов", "lat": 47.2445, "lng": 39.7234, "amenities": {"toilet": True, "shower": True, "cafe": True, "wifi": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Лукойл, Батайск", "lat": 47.1456, "lng": 39.7512, "amenities": {"toilet": True, "cafe": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Газпромнефть, М4 1090 км", "lat": 47.1389, "lng": 39.7423, "amenities": {"toilet": True, "shower": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Лукойл, Каменск", "lat": 48.3178, "lng": 40.2567, "amenities": {"toilet": True, "cafe": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Роснефть, М4 900 км", "lat": 48.3089, "lng": 40.2434, "amenities": {"toilet": True, "wifi": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Газпромнефть, Каменск", "lat": 48.3234, "lng": 40.2689, "amenities": {"toilet": True, "cafe": True, "shower": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Лукойл, Гуково", "lat": 48.0456, "lng": 39.9512, "amenities": {"toilet": True, "cafe": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Роснефть, М4 920 км", "lat": 48.0389, "lng": 39.9423, "amenities": {"toilet": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Газпромнефть, Зверево", "lat": 48.0234, "lng": 40.1123, "amenities": {"toilet": True, "cafe": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Лукойл, М4 925 км", "lat": 48.0156, "lng": 40.1034, "amenities": {"toilet": True, "wifi": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Лукойл, Волгодонск", "lat": 47.5123, "lng": 42.1567, "amenities": {"toilet": True, "cafe": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Роснефть, Волгодонск", "lat": 47.5056, "lng": 42.1434, "amenities": {"toilet": True, "shower": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Лукойл, Таганрог", "lat": 47.2267, "lng": 38.8956, "amenities": {"toilet": True, "cafe": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Газпромнефть, Таганрог", "lat": 47.2189, "lng": 38.8823, "amenities": {"toilet": True, "wifi": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Роснефть, Азов", "lat": 47.1089, "lng": 39.4234, "amenities": {"toilet": True, "cafe": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Лукойл, Азов", "lat": 47.1156, "lng": 39.4312, "amenities": {"toilet": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Лукойл, Сальск", "lat": 46.4623, "lng": 41.5367, "amenities": {"toilet": True, "cafe": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Роснефть, Сальск", "lat": 46.4556, "lng": 41.5234, "amenities": {"toilet": True, "shower": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Газпромнефть, М4 950 км", "lat": 47.6234, "lng": 40.1456, "amenities": {"toilet": True, "cafe": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Лукойл, М4 960 км", "lat": 47.5689, "lng": 40.0923, "amenities": {"toilet": True, "wifi": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Shell, М4 980 км", "lat": 47.4912, "lng": 40.0234, "amenities": {"toilet": True, "cafe": True, "shower": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "BP, М4 1000 км", "lat": 47.4234, "lng": 39.9567, "amenities": {"toilet": True, "cafe": True, "wifi": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Газпромнефть, М4 1050 км", "lat": 47.3456, "lng": 39.8912, "amenities": {"toilet": True, "shower": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Лукойл, М4 1080 км", "lat": 47.2812, "lng": 39.8234, "amenities": {"toilet": True, "cafe": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Роснефть, М4 1100 км", "lat": 47.2123, "lng": 39.7456, "amenities": {"toilet": True, "wifi": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
        {"name": "Shell, М4 1110 км", "lat": 47.1789, "lng": 39.7123, "amenities": {"toilet": True, "cafe": True, "shower": True}, "fuels": {"92": "green", "95": "green", "dt": "green"}},
    ]
    
    db = SessionLocal()
    count = 0
    
    for data in stations_data:
        existing = db.query(Station).filter(
            Station.lat.between(data['lat'] - 0.001, data['lat'] + 0.001),
            Station.lng.between(data['lng'] - 0.001, data['lng'] + 0.001)
        ).first()
        
        if existing:
            continue
        
        station = Station(**data)
        db.add(station)
        count += 1
        
        if count % 10 == 0:
            db.commit()
            print(f"  ✅ Сохранено {count}...")
    
    db.commit()
    db.close()
    
    print(f"\n🎉 Добавлено {count} АЗС на М4!")

if __name__ == "__main__":
    add_m4_realistic_stations()