#weather report
import requests

def get_real_weather(city):
    url = f"https://wttr.in/{city}?format=j1&lang=ko"
    
    try:
        response = requests.get(url)
        
        # 도시를 찾을 수 없거나 통신 에러가 발생한 경우 예외 처리
        if response.status_code != 200:
            print(f"❌ '{city}' 도시를 찾을 수 없거나 서버 통신에 실패했습니다. 영문(예: Seoul, London)으로 다시 시도해보세요.")
            return

        data = response.json()
        print(f"\n🌍 [{city}]의 2일간 실제 일기예보 🌍\n")
        
    
        for i in range(2):
            day_data = data['weather'][i]
            date = day_data['date']
            
            noon_data = day_data['hourly'][4]
            
            if 'lang_ko' in noon_data and noon_data['lang_ko']:
                weather_desc = noon_data['lang_ko'][0]['value']
            else:
                weather_desc = noon_data['weatherDesc'][0]['value']
            
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