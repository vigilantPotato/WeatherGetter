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
                self.temperature_max.append(w['temperature']['max']['celsius'] + '℃')
            except:
                self.temperature_max.append('-')

            #temperature-min-celsiusキーで、最低気温を℃で取得
            try:
                self.temperature_min.append(w['temperature']['min']['celsius'] + '℃')
            except:
                self.temperature_min.append('-')

class ShowWeather(tkinter.LabelFrame):
    '''
    天気予報を表示するクラス
    '''
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widget()    #ラベル、ボタンウィジェットを生成
        self.show_weather()     #天気予報を取得し、ラベルに表示

    def create_widget(self):
        f1 = tkinter.Frame(self)
        l = tkinter.Label(master=f1, text='', width=5, relief=tkinter.RAISED)
        l.grid(row=0, column=0)
        l = tkinter.Label(master=f1, text='今日', width=8, relief=tkinter.RAISED)
        l.grid(row=0, column=1)
        l = tkinter.Label(master=f1, text='明日', width=8, relief=tkinter.RAISED)
        l.grid(row=0, column=2)
        l = tkinter.Label(master=f1, text='明後日', width=8, relief=tkinter.RAISED)
        l.grid(row=0, column=3)

        f2 = tkinter.Frame(self)
        l = tkinter.Label(master=f2, text='天気', width=5, relief=tkinter.RAISED)
        l.grid(row=0, column=0)
        l = tkinter.Label(master=f2, text='max', width=5, relief=tkinter.RAISED)
        l.grid(row=1, column=0)
        l = tkinter.Label(master=f2, text='min', width=5, relief=tkinter.RAISED)
        l.grid(row=2, column=0)

        f3 = tkinter.Frame(self)
        self.label_list = []
        for i in range(3):
            for j in range(3):
                l = tkinter.Label(master=f3, width=8, relief=tkinter.RAISED)
                l.grid(row=i, column=j)
                self.label_list.append(l)
        
        #フレームの表示
        f1.grid(row=0,column=0,columnspan=2)
        f2.grid(row=1,column=0)
        f3.grid(row=1,column=1)

        b = tkinter.Button(self, text='Reflesh', command=self.show_weather)
        b.grid(row=2, columnspan=2, sticky=tkinter.E)

    def show_weather(self):
        place = {'city' :'140010'}  #横浜市
        self.w = GetWeather(place)  #GetWeatherオブジェクト生成
        self.w.get_weather()        #天気、気温情報を取得

        #天気予報表示
        for i, l in enumerate(self.w.weather):
            self.label_list[i]["text"] = l
            self.label_list[i+3]["text"] = self.w.temperature_max[i]
            self.label_list[i+6]["text"] = self.w.temperature_min[i]

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title('WeatherGetter') 
    app = ShowWeather(master=root)
    app.pack()
    root.mainloop()