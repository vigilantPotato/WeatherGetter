import requests
import tkinter

class GetWeather():
    '''
    livedoorのAPIから、天気予報データを取得するクラス
    '''
    url = 'http://weather.livedoor.com/forecast/webservice/json/v1'

    def __init__(self, place):
        self.weather_data = requests.get(self.url, place).json()

    def get_weather(self):
        self.weather = []           #天気（晴れ、雨など）
        self.temperature_max = []   #最高気温
        self.temperature_min = []   #最低気温
        for w in self.weather_data['forecasts']:
            #telopキーで天気を取得
            self.weather.append(w['telop'])
            
            #temperature-max-celsiusキーで、最高気温を℃で取得
            try:
                self.temperature_max.append(w['temperature']['max']['celsius'])
            except:
                self.temperature_max.append('-')

            #temperature-min-celsiusキーで、最低気温を℃で取得
            try:
                self.temperature_min.append(w['temperature']['min']['celsius'])
            except:
                self.temperature_min.append('-')

class Show(tkinter.LabelFrame):
    '''
    場所を選択し、天気予報を表示するクラス
    '''
    pass


if __name__ == "__main__":
    place = {'city' :'140010'}
    w = GetWeather(place)
    w.get_weather()
    print(w.weather)
    print(w.temperature_max)
    print(w.temperature_min)