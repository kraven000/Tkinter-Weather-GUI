from tkinter import Tk,Label,Entry,Button,Frame,PhotoImage,StringVar
from tkinter.messagebox import showerror
from requests import get
from json import loads,dumps
from pytz import timezone
from datetime import datetime
from main import weather


class WeatherApp:
    def __init__(self):
        try:
            with open("account.json","r") as file:
                data = loads(file.read())['api_key']
                self.API_KEY = data
        except:
            pass
        
        
        self.response = self.default_location()
        self.degree_symbol = u"\u00b0"
        self.window = Tk()
        self.time_text = Label(font="Helvetica 20 bold",bg="#101010",fg="#FFFFFF")
        self.store_location = StringVar()
        self.weather_show = Label(self.window,font="Helvetica 60 bold",fg="#FFFFFF",bg="#101010")
        self.location_city_region = Label(self.window,font="Helvetica 16 bold",bg="#101010",fg="#FFFFFF")
        self.weather_condition = Label(self.window,font="Consolas 12 bold",bg="#101010",fg="#FFFFFF")
        self.below_details = Frame(self.window,bg="#0066CC",width=1300,height=120)
        self.windspeed = Label(self.below_details,bg="#0066CC",fg="#202020",font="default 16 bold")
        self.humidity = Label(self.below_details,bg="#0066CC",fg="#202020",font="default 16 bold")
        self.feels_like = Label(self.below_details,bg="#0066CC",fg="#202020",font="default 16 bold")
        self.pressure = Label(self.below_details,bg="#0066CC",fg="#202020",font="default 16 bold")
        self.air_quality_frame = Frame(self.window,width=300,height=265)
        self.aqi_co = Label(self.air_quality_frame,font="Roboto 14 bold")
        self.aqi_no2 = Label(self.air_quality_frame,font="Roboto 14 bold")
        self.aqi_o3 = Label(self.air_quality_frame,font="Roboto 14 bold")
        self.aqi_so2 = Label(self.air_quality_frame,font="Roboto 14 bold")
        self.aqi_pm2_5 = Label(self.air_quality_frame,font="Roboto 14 bold")
        self.aqi_pm10 = Label(self.air_quality_frame,font="Roboto 14 bold")
        self.aqi_gb_defra_index = Label(self.air_quality_frame,font="Roboto 14 bold")
        self.celsius_fahrenhiet_button = Button(self.window,text=f"{self.degree_symbol}F",font="Helvetica 50 bold",fg="#FFFFFF",
                                        bg="#101010",border=0,borderwidth=0,width=2,command=self.fahrenhiet)
        self.quality = Label(self.air_quality_frame,font="Roboto 14 bold")
    
    
    def default_location(self):
        location = get(("https://ipinfo.io/json")).json()
        location = location["loc"]
        # weather
        url = get(f"https://api.weatherapi.com/v1/current.json?key={self.API_KEY}&q={location}&aqi=yes").json()
        del location
        return url
    
    
    def weather(self,events=None):
        try:
            if len(self.store_location.get()) != 0:
                try:
                    # editing location to make it fit for url
                    location = str(self.store_location.get()).strip().lower()
                    location = location.replace(" ", "%20")
                    
                    # json file of weather
                    url_response = get(url=f"https://api.weatherapi.com/v1/current.json?key={self.API_KEY}&q={location}&aqi=yes").json()
                    del location
                    
                    #time with different timezones
                    time = datetime.now(timezone(url_response["location"]["tz_id"])).strftime("%I:%M %p")
                    
                    self.celsius_fahrenhiet_button.place(x=710,y=100)
                    
                    # Adding time and 'Current Weather' text
                    self.time_text.config(text=f"{time} ")
                    
                    # changing location and region
                    self.location_city_region.config(text=f"""{url_response["location"]["name"]}, {url_response["location"]["region"]}, {url_response["location"]["country"]}""")
                    
                    
                    # adding weather in degree celsius
                    self.weather_show.config(text=f"""{url_response["current"]["temp_c"]}{self.degree_symbol}C /""",font="Helvetica 60 bold",bg="#101010",fg="#FFFFFF")
                    
                    
                    # adding condition            
                    self.weather_condition.config(text=f"""Feels Like:- {url_response['current']['condition']['text']}""",font="Consolas 12 bold",bg="#101010",fg="#FFFFFF")
                    
                    
                    # adding the details of bluebox
                    self.windspeed.config(text=f"""{url_response["current"]["wind_kph"]} km/hr""",bg="#0066CC",fg="#202020",font="default 16 bold")
                    self.pressure.config(text=f"""{url_response["current"]["pressure_mb"]} mb""",bg="#0066CC",fg="#202020",font="default 16 bold")
                    self.humidity.config(text=f"""{url_response["current"]["humidity"]}%""",bg="#0066CC",fg="#202020",font="default 16 bold")
                    self.feels_like.config(text=f"{url_response['current']['feelslike_c']}",bg="#0066CC",fg="#202020",font="default 16 bold")
                    
                    
                    air_quality = url_response["current"]["air_quality"]
                    if air_quality["gb-defra-index"]>=1 and air_quality["gb-defra-index"]<4:
                        background_color = "#80FF00"
                        self.quality.config(text="Quality:- Low",bg=background_color)
                    elif air_quality["gb-defra-index"]>=4 and air_quality["gb-defra-index"]<7:
                        background_color = "#F2D414"
                        self.quality.config(text="Quality:- Moderate",bg=background_color)
                    elif air_quality["gb-defra-index"]>=7 and air_quality["gb-defra-index"]<10:
                        background_color = "#CC0000"
                        self.quality.config(text="Quality:- High",bg=background_color)
                    elif air_quality["gb-defra-index"]==10:
                        background_color = "#99004C"
                        self.quality.config(text="AQI:- Very High",bg=background_color)
                    
                    
                    self.air_quality_frame.config(bg=background_color)
                    self.aqi_co.config(text=f"""CO:- {air_quality["co"]}""",bg=background_color)
                    self.aqi_no2.config(text=f"""NO2:- {air_quality["no2"]}""",bg=background_color)
                    self.aqi_o3.config(text=f"""O3:- {air_quality["o3"]}""",bg=background_color)
                    self.aqi_so2.config(text=f"""SO2:- {air_quality["so2"]}""",bg=background_color)
                    self.aqi_pm2_5.config(text=f"""PM 2.5:- {air_quality["pm2_5"]}""",bg=background_color)
                    self.aqi_pm10.config(text=f"""PM 10:- {air_quality["pm10"]}""",bg=background_color)
                    self.aqi_gb_defra_index.config(text=f"""GB Defra Index:- {air_quality["gb-defra-index"]}""",bg=background_color)
                    
                    del air_quality
                    self.response = url_response
                    return url_response
                
                except KeyError:
                    self.celsius_fahrenhiet_button.place_forget()
                    self.weather_show.config(text="This Location doesn't Exist",font="Helvetica 16 bold")
                    self.location_city_region.config(text="ERROR")
                    
            else:
                self.default_location()
        
        except:
            self.default_location()
    
    # def temp(self):
    #     with open("temp.json","r") as file:
    #         return loads(file.read())
    
    
    def celsius(self):
        '''The function to show weather in Degree Celsius if button is pressed'''
        
        self.celsius_fahrenhiet_button.config(text=f"{self.degree_symbol}F",command=self.fahrenhiet)
        self.weather_show.config(text=f"{self.response["current"]["temp_c"]}{self.degree_symbol}C /")
        self.feels_like.config(text=f"{self.response['current']['feelslike_c']}{self.degree_symbol}C")


    def fahrenhiet(self):
        '''The function to show weather in Fahrenhiet when button is pressed'''
        
        self.celsius_fahrenhiet_button.config(text=f"{self.degree_symbol}C",command=self.celsius)
        self.weather_show.config(text=f"{self.response['current']['temp_f']}{self.degree_symbol}F /")
        self.feels_like.config(text=f"{self.response['current']['feelslike_f']}{self.degree_symbol}F")


    def buildui(self):
        
        # root.iconphoto(True,icon)
        self.window.title("Weather App")
        self.window.geometry("1220x505")
        self.window.resizable(False,False)
        self.window.configure(bg="#101010")
        
        # Images
        gui_icon = PhotoImage(file="icon.png")
        weather_icon = PhotoImage(file="weather_icon.png")
        search_icon = PhotoImage(file="search_icon.png")
        location_icon = PhotoImage(file="location_icon.png")
        
        # Icon
        self.window.iconphoto(False,gui_icon)
        
        #entry widget
        entry_widget = Entry(self.window,textvariable=self.store_location,width=24,justify="center",background="#404040",foreground="#FFFFFF",border=0,font="Consolas 25 bold")
        entry_widget.place(x=10,y=10)
        entry_widget.bind("<Return>",self.weather)
        entry_widget.focus()
        
        # i am declaring default response as global to avoid calling weather soo many time and only calling it one time
        # default_response = weather()
        
        
        #button for search
        Button(self.window,image=search_icon,bg="#101010",borderwidth=0,border=0,command=self.weather).place(x=450,y=6)
        
        # current weather text to show after user press search button or enter
        current_weather_text = Label(self.window,text="Current Weather",font="Helvetica 20 bold",bg="#101010",fg="#FFFFFF")
        current_weather_text.place(x=6,y=60)
        
        # to show current time when press search button or enter
        time = datetime.now(timezone(self.response["location"]["tz_id"])).strftime("%I:%M %p")
        self.time_text.place(x=6,y=100)
        self.time_text.config(text=time)
        
        # to show city and region
        Label(image=location_icon,bg="#101010").place(x=510,y=6)
        
        self.location_city_region.place(x=560,y=12)
        self.location_city_region.config(text=f"""{self.response["location"]["name"]}, {self.response["location"]["region"]}, {self.response["location"]["country"]}""")
        
        # showing weather icon
        Label(self.window,image=weather_icon,bg="#101010").place(x=160,y=100)
        
        # showing weather
        self.weather_show.place(x=412,y=115)
        self.weather_show.config(text=f"{self.response["current"]["temp_c"]}{self.degree_symbol}C /")
        
        # showing condition
        
        self.weather_condition.place(x=422,y=200)
        self.weather_condition.config(text=f"""Condition:- {self.response['current']['condition']['text']}""")
        
        # Button to switch between degree celsius and degree fahrenheit
        self.celsius_fahrenhiet_button.place(x=710,y=100)
        self.celsius_fahrenhiet_button.config(text=f"{self.degree_symbol}F",command=self.fahrenhiet)
        
        
        self.below_details.place(x=-10,y=390)
        
        # To show Wind Speed, Humidity, Description and Pressure
        Label(self.below_details,text="""WIND SPEED                                HUMIDITY                                FEELS LIKE                                PRESSURE""",font="Default 18 bold",fg="#FFFFFF",bg="#0066CC",border=0,borderwidth=0).place(x=10,y=10)
        
        self.windspeed.config(text=f"""{self.response['current']['wind_kph']} km/hr""")
        self.windspeed.place(x=15,y=70)
        
        self.humidity.config(text=f"""{self.response['current']['humidity']}%""")
        self.humidity.place(x=415,y=70)
        
        self.feels_like.config(text=f"""{self.response['current']['feelslike_c']}{self.degree_symbol}C""")
        self.feels_like.place(x=770,y=70)
        
        self.pressure.config(text=f"""{self.response['current']['pressure_mb']} mb""")
        self.pressure.place(x=1110,y=70)
        
        
        # To show air quality
        air_quality_index = self.response["current"]["air_quality"]["gb-defra-index"]
        quality_text = None
        background_color = None
        if air_quality_index>=1 and air_quality_index<4:
            background_color = "#80FF00"
            quality_text = "AQI:- Low"
            
        elif air_quality_index>=4 and air_quality_index<7:
            background_color = "#F2D414"
            quality_text = "AQI:- Moderate"
            
        elif air_quality_index>=7 and air_quality_index<10:
            background_color = "#CC0000"
            quality_text = "AQI:- High"
            
        elif air_quality_index==10:
            background_color = "#99004C"
            quality_text = "AQI:- Very High"
            
        
        self.air_quality_frame.config(bg=background_color)
        self.air_quality_frame.place(x=850,y=50)
        
        
        self.aqi_co.config(text=f"""CO:- {self.response["current"]["air_quality"]["co"]}""",bg=background_color)
        self.aqi_co.place(x=0,y=5)
        
        self.aqi_no2.config(text=f"""NO2:- {self.response["current"]["air_quality"]["no2"]}""",bg=background_color)
        self.aqi_no2.place(x=0,y=38)
        
        
        self.aqi_o3.place(x=0,y=71)
        self.aqi_o3.config(text=f"""O3:- {self.response["current"]["air_quality"]["o3"]}""",bg=background_color)
        
        self.aqi_so2.place(x=0,y=104)
        self.aqi_so2.config(text=f"""SO2:- {self.response["current"]["air_quality"]["so2"]}""",bg=background_color)
        
        self.aqi_pm2_5.place(x=0,y=137)
        self.aqi_pm2_5.config(text=f"""PM 2.5:- {self.response["current"]["air_quality"]["pm2_5"]}""",bg=background_color)
        
        self.aqi_pm10.place(x=0,y=170)
        self.aqi_pm10.config(text=f"""PM 10:- {self.response["current"]["air_quality"]["pm10"]}""",bg=background_color)
        
        self.aqi_gb_defra_index.place(x=0,y=203)
        self.aqi_gb_defra_index.config(text=f"""GB Defra Index:- {self.response["current"]["air_quality"]["gb-defra-index"]}""",bg=background_color)
        
        self.quality.place(x=0,y=236)
        self.quality.config(text=quality_text,bg=background_color)
        
        self.window.mainloop()


if __name__ == '__main__':
    f = WeatherApp()
    f.buildui()