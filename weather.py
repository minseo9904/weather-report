import requests
from datetime import datetime

print("날씨 예보 프로그램")

city = input("날씨를 확인할 지역을 입력하세요 (기본값: 서울): ")

if city == "":
    city = "서울"

print("입력한 지역:", city)

if city == "서울":
    latitude = 37.5665
    longitude = 126.9780
else:
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"


    geo_params = {
        "name": city,
        "count": 1,
        "format": "json",
        "language": "ko"
    }

    geo_response = requests.get(geo_url, params=geo_params)
    geo_data = geo_response.json()

    if "results" not in geo_data or len(geo_data["results"]) == 0:
        print("지역을 찾을 수 없습니다.")
        exit()

    latitude = geo_data["results"][0]["latitude"]
    longitude = geo_data["results"][0]["longitude"]

print("위도:", latitude)
print("경도:", longitude)

weather_url = "https://api.open-meteo.com/v1/forecast"

weather_params = {
    "latitude": latitude,
    "longitude": longitude,
    "hourly": "temperature_2m,precipitation_probability,relative_humidity_2m,wind_speed_10m,weather_code",
    "daily": "temperature_2m_max,temperature_2m_min",
    "forecast_days": 3,
    "timezone": "Asia/Seoul"
}

weather_response = requests.get(weather_url, params=weather_params)

weather_data = weather_response.json()
daily_times = weather_data["daily"]["time"]
max_temperatures = weather_data["daily"]["temperature_2m_max"]
min_temperatures = weather_data["daily"]["temperature_2m_min"]

times = weather_data["hourly"]["time"]
temperatures = weather_data["hourly"]["temperature_2m"]
precipitation = weather_data["hourly"]["precipitation_probability"]
humidity = weather_data["hourly"]["relative_humidity_2m"]
wind_speed = weather_data["hourly"]["wind_speed_10m"]
weather_code = weather_data["hourly"]["weather_code"]

today = datetime.now().date()

weather_names = {
    0: "☀️ 맑음",
    1: "🌤️ 대체로 맑음",
    2: "⛅ 부분적으로 흐림",
    3: "☁️ 흐림",
    45: "🌫️ 안개",
    48: "🌫️ 짙은 안개",
    51: "🌦️ 약한 이슬비",
    53: "🌦️ 이슬비",
    55: "🌧️ 강한 이슬비",
    61: "🌧️ 약한 비",
    63: "🌧️ 비",
    65: "🌧️ 강한 비",
    71: "🌨️ 약한 눈",
    73: "❄️ 눈",
    75: "❄️ 강한 눈",
    80: "🌦️ 약한 소나기",
    81: "🌧️ 소나기",
    82: "🌧️ 강한 소나기",
    95: "⛈️ 뇌우",
    96: "⛈️ 우박을 동반한 뇌우",
    99: "⛈️ 강한 우박을 동반한 뇌우"
}

last_day = ""

for i in range(len(times)):
    if times[i].endswith("T06:00") or times[i].endswith("T15:00"):
        date = times[i].split("T")[0]
        time = times[i].split("T")[1]

        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        day_diff = (date_obj - today).days

        if day_diff == 0:
            day = "오늘"
        elif day_diff == 1:
            day = "내일"
        elif day_diff == 2:
            day = "모레"
        else:
            day = date

        daily_index = day_diff

        max_temp = max_temperatures[daily_index]
        min_temp = min_temperatures[daily_index]

        weather = weather_names.get(weather_code[i], "알 수 없음")

        if day != last_day:
            print()
            print("====================")
            print("       ", day)
            print("====================")
            print("최저기온:", min_temp, "℃")
            print("최고기온:", max_temp, "℃")
            last_day = day

        print()
        print("[", time, "]")
        print("날씨:", weather)
        print("기온:", temperatures[i], "℃")
        print("강수확률:", precipitation[i], "%")
        print("습도:", humidity[i], "%")
        print("풍속:", wind_speed[i], "km/h")