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
            with open("account.json","rb") as file:
                data = loads(file)
                self.API_KEY = data
        except:
            self.info_window()
        
        self.location = None
    
    
    def weather(events=None):
        try:
            if len(store_area.get()) != 0:
                try:
                    
                    # editing location to make it fit for url
                    location = str(store_area.get()).strip().lower()
                    location = location.replace(" ", "%20")
                    
                    # json file of weather
                    url_response = get(url=f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&aqi=yes").json()
                    del location
                    
                    
                    #time with different timezones
                    time = datetime.now(timezone(url_response["location"]["tz_id"])).strftime("%I:%M %p")
                    
                    
                    # Adding time and 'Current Weather' text
                    time_text.config(text=f"{time} ")
                    current_weather_text.config(text="Current Weather")
                    
                    
                    # degree symbol
                    degree_symbol = u"\u00b0"
                    
                    
                    # changing location and region
                    location_city_region.config(text=f"""{url_response["location"]["name"]}, {url_response["location"]["region"]}, {url_response["location"]["country"]}""")
                    
                    
                    # adding weather in degree celsius
                    weather_show.config(text=f"""{url_response["current"]["temp_c"]}{degree_symbol}C /""",font="Helvetica 60 bold",bg="#101010",fg="#FFFFFF")
                    
                    
                    # adding condition            
                    weather_condition.config(text=f"""Feels Like:- {url_response["current"]["feelslike_c"]}{degree_symbol}C""",font="Consolas 12 bold",bg="#101010",fg="#FFFFFF")
                    
                    # if len(str(url_response["current"]["temp_c"]))==3:
                    #     celsius_fahrenhiet_button.place(x=680,y=110)
                    # else:
                    #     celsius_fahrenhiet_button.place(x=690,y=110)
                    
                    
                    # adding the details of bluebox
                    windspeed.config(text=f"""{url_response["current"]["wind_kph"]} km/hr""",bg="#0066CC",fg="#202020",font="default 16 bold")
                    pressure.config(text=f"""{url_response["current"]["pressure_mb"]} mb""",bg="#0066CC",fg="#202020",font="default 16 bold")
                    humidity.config(text=f"""{url_response["current"]["humidity"]}%""",bg="#0066CC",fg="#202020",font="default 16 bold")
                    
                    
                    weather_condition_for_bluerect = str(url_response["current"]["condition"]["text"]).split()
                    
                    if len(weather_condition_for_bluerect)>1:
                        weather_condition_for_bluerect = weather_condition_for_bluerect[0]+" "+weather_condition_for_bluerect[1]
                    else:
                        weather_condition_for_bluerect = weather_condition_for_bluerect[0]
                    
                    condition.config(text=f"""{weather_condition_for_bluerect}""",bg="#0066CC",fg="#202020",font="default 16 bold")
                    
                    del weather_condition_for_bluerect
                    
                    air_quality = url_response["current"]["air_quality"]
                    if air_quality["gb-defra-index"]>=1 and air_quality["gb-defra-index"]<4:
                        background_color = "#80FF00"
                        quality.config(text="Quality:- Low",bg=background_color)
                    elif air_quality["gb-defra-index"]>=4 and air_quality["gb-defra-index"]<7:
                        background_color = "#F2D414"
                        quality.config(text="Quality:- Moderate",bg=background_color)
                    elif air_quality["gb-defra-index"]>=7 and air_quality["gb-defra-index"]<10:
                        background_color = "#CC0000"
                        quality.config(text="Quality:- High",bg=background_color)
                    elif air_quality["gb-defra-index"]==10:
                        background_color = "#99004C"
                        quality.config(text="AQI:- Very High",bg=background_color)
                    
                    
                    air_quality_frame.config(bg=background_color)
                    aqi_co.config(text=f"""CO:- {air_quality["co"]}""",bg=background_color)
                    aqi_no2.config(text=f"""NO2:- {air_quality["no2"]}""",bg=background_color)
                    aqi_o3.config(text=f"""O3:- {air_quality["o3"]}""",bg=background_color)
                    aqi_so2.config(text=f"""SO2:- {air_quality["so2"]}""",bg=background_color)
                    aqi_pm2_5.config(text=f"""PM 2.5:- {air_quality["pm2_5"]}""",bg=background_color)
                    aqi_pm10.config(text=f"""PM 10:- {air_quality["pm10"]}""",bg=background_color)
                    aqi_gb_defra_index.config(text=f"""GB Defra Index:- {air_quality["gb-defra-index"]}""",bg=background_color)
                    
                    del air_quality
                    return url_response
                
                except KeyError:
                    celsius_fahrenhiet_button.place_forget()
                    weather_show.config(text="This Location doesn't Exist",font="Helvetica 30 bold")
                    location_city_region.config(text="ERROR")
                    
            else:
                
                location = get(("https://ipinfo.io/json")).json()
                location = location["loc"]
                # weather
                url = get(f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&aqi=yes").json()
                del location
                return url
        
        except:
            
            location = get(("https://ipinfo.io/json")).json()
            location = location["loc"]
            # weather
            url = get(f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&aqi=yes").json()
            del location
            return url
    
    
    def celsius(self):
        '''The function to show weather in Degree Celsius if button is pressed'''
        
        response = weather()
        degree_symbol = u"\u00b0"
        
        celsius_fahrenhiet_button.config(text=f"{degree_symbol}F")
        
        celsius_fahrenhiet_button.config(command=self.fahrenhiet,bg="#101010",fg="#FFFFFF")
        
        weather_show.config(text=f"""{response["current"]["temp_c"]}{degree_symbol}C /""",font="Helvetica 60 bold",bg="#101010",fg="#FFFFFF")
        weather_condition.config(text=f"""Feels Like:- {response["current"]["feelslike_c"]}{degree_symbol}C""",font="Consolas 14 bold",bg="#101010",fg="#FFFFFF")


    def fahrenhiet(self):
        '''The function to show weather in Fahrenhiet when button is pressed'''
        
        response = weather()
        degree_symbol = u"\u00b0"
        
        celsius_fahrenhiet_button.config(text=f"{degree_symbol}C")
        
        celsius_fahrenhiet_button.config(command=self.celsius,bg='#101010',fg="#FFFFFF")
        
        weather_show.config(text=f"""{response["current"]["temp_f"]}{degree_symbol}F /""",font="Helvetica 60 bold",bg="#101010",fg="#FFFFFF")
        weather_condition.config(text=f"""Feels Like:- {response["current"]["feelslike_f"]}{degree_symbol}F""",font="Consolas 14 bold",bg="#101010",fg="#FFFFFF")
    
    
    def buildui(self):
        response = weather()
        global time_text, current_weather_text, weather_show, store_area, weather_condition, detailed_desc, windspeed, condition, pressure, humidity, celsius_fahrenhiet_button, weather_show,location_city_region,air_quality_frame,aqi_co,aqi_no2,aqi_o3,aqi_pm2_5,aqi_pm10,aqi_gb_defra_index,aqi_so2,quality
        
        
        # root.iconphoto(True,icon)
        root = Tk()
        root.title("Weather App")
        root.geometry("1220x505")
        root.resizable(False,False)
        root.configure(bg="#101010")
        
        # Images
        gui_icon = PhotoImage(file="icon.png")
        weather_icon = PhotoImage(file="weather_icon.png")
        search_icon = PhotoImage(file="search_icon.png")
        location_icon = PhotoImage(file="location_icon.png")
        
        # Icon
        root.iconphoto(False,gui_icon)
        
        #entry widget
        store_area = StringVar()
        entry_widget = Entry(root,textvariable=store_area,width=24,justify="center",background="#404040",foreground="#FFFFFF",border=0,font="Consolas 25 bold")
        entry_widget.place(x=10,y=10)
        entry_widget.bind("<Return>",weather)
        entry_widget.focus()
        
        # i am declaring default response as global to avoid calling weather soo many time and only calling it one time
        # default_response = weather()
        
        
        #button for search
        Button(root,image=search_icon,bg="#101010",borderwidth=0,border=0,command=weather).place(x=450,y=6)
        
        # current weather text to show after user press search button or enter
        current_weather_text = Label(root,text="Current Weather",font="Helvetica 20 bold",bg="#101010",fg="#FFFFFF")
        current_weather_text.place(x=6,y=60)
        
        # to show current time when press search button or enter
        time = datetime.now(timezone(response["location"]["tz_id"])).strftime("%I:%M %p")
        time_text = Label(root,text=time,font="Helvetica 20 bold",bg="#101010",fg="#FFFFFF")
        time_text.place(x=6,y=100)
        
        # to show city and region
        Label(image=location_icon,bg="#101010").place(x=520,y=6)
        
        location_city_region = Label(root,text=f"""{response["location"]["name"]}, {response["location"]["region"]}, {response["location"]["country"]}""",font="Helvetica 16 bold",bg="#101010",fg="#FFFFFF")
        location_city_region.place(x=565,y=12)
        
        # showing weather icon
        Label(root,image=weather_icon,bg="#101010").place(x=160,y=100)
        
        # showing weather
        degree_symbol = u"\u00b0"
        weather_show = Label(root,text=f"""{response["current"]["temp_c"]}{degree_symbol}C /""",font="Helvetica 60 bold",fg="#FFFFFF",bg="#101010")
        weather_show.place(x=412,y=115)
        
        # showing condition
        weather_condition = Label(root,text=f"""Feels Like:- {response["current"]["feelslike_c"]}{degree_symbol}C""",font="Consolas 12 bold",bg="#101010",fg="#FFFFFF")
        weather_condition.place(x=422,y=200)
        
        # Button to switch between degree celsius and degree fahrenheit
        celsius_fahrenhiet_button = Button(root,text=f"{degree_symbol}F",font="Helvetica 50 bold",fg="#FFFFFF",
                                        bg="#101010",border=0,borderwidth=0,width=2,command=self.fahrenhiet)
        celsius_fahrenhiet_button.place(x=710,y=100)
        # if len(str(default_response["current"]["temp_c"]))==3:
        #     celsius_fahrenhiet_button.place(x=680,y=110)
        # else:
        #     celsius_fahrenhiet_button.place(x=705,y=110)
        
        
        # short description
        # Frame for Background
        Frame(root,bg="#0066CC",width=1300,height=120).place(x=-10,y=390)
        
        # To show Wind Speed, Humidity, Description and Pressure
        Label(root,text="WIND SPEED                  HUMIDITY                  DESCRIPTION                            PRESSURE",font="Default 18 bold",fg="#FFFFFF",bg="#0066CC",border=0,borderwidth=0).place(x=0,y=400)
        
        windspeed = Label(root,text=f"""{response["current"]["wind_kph"]} km/hr""",bg="#0066CC",fg="#202020",font="default 16 bold")
        windspeed.place(x=5,y=450)
        
        humidity = Label(root,text=f"""{response["current"]["humidity"]}%""",bg="#0066CC",fg="#202020",font="default 16 bold")
        humidity.place(x=318,y=450)
        
        condition = Label(root,text=f"""{response["current"]["condition"]["text"]}""",bg="#0066CC",fg="#202020",font="default 16 bold")
        condition.place(x=590,y=450)
        
        pressure = Label(root,text=f"""{response["current"]["pressure_mb"]} mb""",bg="#0066CC",fg="#202020",font="default 16 bold")
        pressure.place(x=1000,y=450)
        
        
        # To show air quality
        air_quality_index = response["current"]["air_quality"]["gb-defra-index"]
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
            
        
        
        air_quality_frame = Frame(root,width=300,height=265,bg=background_color)
        air_quality_frame.place(x=850,y=50)
        
        
        aqi_co = Label(root,text=f"""CO:- {response["current"]["air_quality"]["co"]}""",font="Roboto 14 bold",bg=background_color)
        aqi_co.place(x=852,y=50)
        
        aqi_no2 = Label(root,text=f"""NO2:- {response["current"]["air_quality"]["no2"]}""",font="Roboto 14 bold",bg=background_color)
        aqi_no2.place(x=852,y=80)
        
        aqi_o3 = Label(root,text=f"""O3:- {response["current"]["air_quality"]["o3"]}""",font="Roboto 14 bold",bg=background_color)
        aqi_o3.place(x=852,y=110)
        
        aqi_so2 = Label(root,text=f"""SO2:- {response["current"]["air_quality"]["so2"]}""",font="Roboto 14 bold",bg=background_color)
        aqi_so2.place(x=852,y=140)
        
        aqi_pm2_5 = Label(root,text=f"""PM 2.5:- {response["current"]["air_quality"]["pm2_5"]}""",font="Roboto 14 bold",bg=background_color)
        aqi_pm2_5.place(x=852,y=170)
        
        aqi_pm10 = Label(root,text=f"""PM 10:- {response["current"]["air_quality"]["pm10"]}""",font="Roboto 14 bold",bg=background_color)
        aqi_pm10.place(x=852,y=200)
        
        aqi_gb_defra_index = Label(root,text=f"""GB Defra Index:- {response["current"]["air_quality"]["gb-defra-index"]}""",font="Roboto 14 bold",bg=background_color)
        aqi_gb_defra_index.place(x=852,y=230)
        
        quality = Label(root,text=quality_text,bg=background_color,font="Roboto 14 bold")
        quality.place(x=852,y=260)
        
        root.mainloop()


if __name__ == '__main__':
    f = WeatherApp()
    f.buildui()