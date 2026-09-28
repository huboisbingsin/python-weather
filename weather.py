import requests

def get_real_weather(city):
    url = f"https://wttr.in/{city}?format=j1"
    
    # 딕셔너리의 모든 키를 소문자로 통일
    weather_translation = {
        "clear": "맑음",
        "sunny": "맑음",
        "partly cloudy": "구름 조금",
        "cloudy": "흐림",
        "overcast": "잔뜩 흐림",
        "mist": "옅은 안개",
        "fog": "짙은 안개",
        "patchy rain possible": "비 올 가능성 있음",
        "patchy rain nearby": "주변에 비 내림",
        "patchy light rain": "약한 국지성 비",
        "light rain": "약한 비",
        "moderate rain at times": "가끔 보통 비",
        "moderate rain": "보통 비",
        "heavy rain at times": "가끔 강한 비",
        "heavy rain": "강한 비",
        "light drizzle": "약한 이슬비",
        "patchy snow possible": "눈 올 가능성 있음",
        "light snow": "약한 눈",
        "moderate snow": "보통 눈",
        "heavy snow": "강한 눈",
        "thundery outbreaks possible": "뇌우 가능성 있음",
        "moderate or heavy rain shower": "강한 소나기",
        "light rain shower": "가벼운 소나기"
    }

    try:
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"❌ '{city}' 도시를 찾을 수 없거나 서버 통신에 실패했습니다.")
            return

        data = response.json()
        print(f"\n🌍 [{city}]의 2일간 실제 일기예보 🌍\n")
        
        for i in range(2):
            day_data = data['weather'][i]
            date = day_data['date']
            noon_data = day_data['hourly'][4]
            
            # 서버가 주는 영문 날씨 상태를 추출 후 모두 소문자로 변환
            weather_desc_en = noon_data['weatherDesc'][0]['value'].strip().lower()
            
            # 1차 시도: 딕셔너리에서 정확히 일치하는 값 찾기
            weather_desc = weather_translation.get(weather_desc_en)
            
            # 2차 시도: 사전에 없는 표현일 경우 핵심 키워드로 유추하여 번역
            if not weather_desc:
                if "rain" in weather_desc_en or "drizzle" in weather_desc_en:
                    weather_desc = "비"
                elif "snow" in weather_desc_en or "blizzard" in weather_desc_en:
                    weather_desc = "눈"
                elif "cloud" in weather_desc_en or "overcast" in weather_desc_en:
                    weather_desc = "흐림"
                elif "sun" in weather_desc_en or "clear" in weather_desc_en:
                    weather_desc = "맑음"
                elif "fog" in weather_desc_en or "mist" in weather_desc_en:
                    weather_desc = "안개"
                elif "thunder" in weather_desc_en or "storm" in weather_desc_en:
                    weather_desc = "천둥번개"
                else:
                    # 끝까지 예측할 수 없는 단어라면 원래 영문을 출력하여 데이터 누락 방지
                    weather_desc = weather_desc_en
            
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
    city_input = input("일기예보를 확인할 도시 이름을 입력하세요 (예: 서울, 천안, Busan): ")
    get_real_weather(city_input)