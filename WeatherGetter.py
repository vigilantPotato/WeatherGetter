import bs4
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


class GetPlaceData():
    '''
    livedoorのAPIから、都道府県、都市データを取得するクラス
    '''
    def __init__(self):
        path = 'http://weather.livedoor.com/forecast/rss/primary_area.xml'
        self.res = requests.get(path)
        self.get_pref()

    def get_pref(self):
        self.pref_list = []
        b = bs4.BeautifulSoup(self.res.text, 'xml').select('pref')

        for pref in b:
            self.pref_list.append(pref.get('title'))

    def get_city(self, pref):
        self.city_list = []
        self.id_list = []
        select_word = ('pref[title="%s"] city' % pref)
        b = bs4.BeautifulSoup(self.res.text, 'xml').select(select_word)

        for city in b:
            self.city_list.append(city.get('title'))
            self.id_list.append(city.get('id'))

class ShowWeather(tkinter.LabelFrame):
    '''
    天気予報を表示するクラス
    '''
    def __init__(self, master=None):
        super().__init__(master)
        self.place_data = GetPlaceData()    #GetPlaceDataオブジェクト生成
        self.create_widget()                #ラベル、ボタンウィジェットを生成

    def create_widget(self):
        f0 = tkinter.Frame(self)
        #list1
        self.l1 = tkinter.Listbox(f0, width = 15)
        for p in self.place_data.pref_list:
            self.l1.insert(tkinter.END, p)
        self.l1.bind('<ButtonRelease-1>', self.show_city)
        self.l1.grid(row=0, column=0)

        #list2
        self.l2 = tkinter.Listbox(f0, width = 15)
        self.l2.bind('<ButtonRelease-1>', self.get_id)
        self.l2.grid(row=0, column=1)

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
        
        #表示
        f0.grid(row=0, column=0, columnspan=2)
        f1.grid(row=1, column=0, columnspan=2)
        f2.grid(row=2, column=0)
        f3.grid(row=2, column=1)

    def show_city(self, event):
        #list2に選択した都道府県の都市を表示
        self.l2.delete(0, last=tkinter.END)
        index = self.l1.curselection()[0]
        p = self.place_data.pref_list[index]
        self.place_data.get_city(p)
        for c in self.place_data.city_list:
            self.l2.insert(tkinter.END, c)
    
    def get_id(self, event):
        #list2で選択した都市のidを取得
        index = self.l2.curselection()[0]
        city_id = self.place_data.id_list[index]
        self.show_weather(city_id)

    def show_weather(self, city_id):
        place = {'city' : city_id}  #横浜市
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