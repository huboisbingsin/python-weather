import requests # type: ignore

def get_real_weather(city):
    url = f"https://wttr.in/{city}?format=j1&lang=ko"
    
    weather_translation = {
        "Clear": "맑음",
        "Sunny": "맑음",
        "Partly cloudy": "구름 조금",
        "Cloudy": "흐림",
        "Overcast": "잔뜩 흐림",
        "Mist": "옅은 안개",
        "Fog": "짙은 안개",
        "Patchy rain possible": "비 올 가능성 있음",
        "Patchy rain nearby": "주변에 비 내림",
        "Patchy light rain": "약한 국지성 비",
        "Light rain": "약한 비",
        "Moderate rain at times": "가끔 보통 비",
        "Moderate rain": "보통 비",
        "Heavy rain at times": "가끔 강한 비",
        "Heavy rain": "강한 비",
        "Light drizzle": "약한 이슬비",
        "Patchy snow possible": "눈 올 가능성 있음",
        "Light snow": "약한 눈",
        "Moderate snow": "보통 눈",
        "Heavy snow": "강한 눈",
        "Thundery outbreaks possible": "뇌우 가능성 있음",
        "Moderate or heavy rain shower": "보통 또는 강한 소나기"
    }

    try:
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"❌ '{city}' 도시를 찾을 수 없거나 서버 통신에 실패했습니다. 영문(예: Seoul, London)으로 다시 시도해보거나 다른 도시를 입력해주세요.")
            return

        data = response.json()
        print(f"\n🌍 [{city}]의 2일간 실제 일기예보 🌍\n")
        
        for i in range(2):
            day_data = data['weather'][i]
            date = day_data['date']
            
            # 낮 12시(인덱스 4) 기준 데이터 추출
            noon_data = day_data['hourly'][4]
            
            # 1. 서버가 주는 영문 날씨 상태 추출
            weather_desc_en = noon_data['weatherDesc'][0]['value'].strip()
            
            # 2. 서버가 주는 한국어 상태가 존재하는지 확인
            if 'lang_ko' in noon_data and noon_data['lang_ko']:
                weather_desc = noon_data['lang_ko'][0]['value']
            else:
                # 3. 한국어 응답이 없으면 딕셔너리에서 번역 (딕셔너리에 없으면 원래 영문 출력)
                weather_desc = weather_translation.get(weather_desc_en, weather_desc_en)
            
            temp = noon_data['tempC']
            rain_chance = noon_data['chanceofrain']
            humidity = noon_data['humidity']
            wind_speed = noon_data['windspeedKmph']
            
            min_temp = day_data['mintempC']
            max_temp = day_data['maxtempC']
            
            day_label = "오늘" if i == 0 else "내일"
            
            print(f"📅 {day_label} ({date})")
            print(f"  ▪ 날씨: {weather_desc}")
            print(f"  ▪ 기온 (낮 12시 기준): {temp}°C")
            print(f"  ▪ 최저/최고 일일기온: {min_temp}°C / {max_temp}°C")
            print(f"  ▪ 강수 확률: {rain_chance}%")
            print(f"  ▪ 습도: {humidity}%")
            print(f"  ▪ 풍속: {wind_speed} km/h")
            print("-" * 35)

    except Exception as e:
        print("프로그램 실행 중 오류가 발생했습니다:", e)

if __name__ == "__main__":
    city_input = input("일기예보를 확인할 도시 이름을 입력하세요 (예: 서울, 천안, 부산): ")
    get_real_weather(city_input)
    #https://github.com/huboisbingsin/python-weather.git    