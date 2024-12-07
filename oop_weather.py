from tkinter import Tk,Label,Entry,Button,Frame,PhotoImage,StringVar
from tkinter.messagebox import showerror
from requests import get
from pickle import load,dump
import time


DEGREE_SYMBOL = u"\u00b0"

class WeatherApp:
    def __init__(self):
        
        self.API_KEY = None
        self.response = self.default_location()
        self.window = Tk()
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
        self.celsius_fahrenheit_button = Button(self.window,text=f"{DEGREE_SYMBOL}F",
                                                font="Helvetica 50 bold",fg="#FFFFFF",bg="#101010",
                                                border=0,borderwidth=0,width=2,command=self.fahrenheit)
        self.quality = Label(self.air_quality_frame,font="Roboto 14 bold")
        
        self.show_time_widget = Label(self.window,text="",font="Helvetica 20 bold",bg="#101010",
                                      fg="#FFFFFF")
    
    
    def default_location(self):
        location = get(("https://ipinfo.io/json")).json()
        location = location["loc"]
        # weather
        url = get(f"https://api.weatherapi.com/v1/current.json?key={self.API_KEY}&q={location}&aqi=yes").json()
        
        self.response = url
    
    
    def weather(self,events=None):
        try:
            if len(self.store_location.get()) != 0:
                try:
                    
                    # editing location to make it fit for url
                    location = self.store_location.get().strip().lower()
                    location = location.replace(" ", "%20")
                    
                    # json file of weather
                    url_response = get(url=f"https://api.weatherapi.com/v1/current.json?key={self.API_KEY}&q={location}&aqi=yes").json()
                    del location
                    
                    len_of_weather = len(str(url_response['current']['temp_c']))+2
                    if len_of_weather>6:
                        self.celsius_fahrenheit_button.place(x=735,y=100)
                    elif len_of_weather<6:
                        self.celsius_fahrenheit_button.place(x=690,y=100)
                    else:
                        self.celsius_fahrenheit_button.place(x=710,y=100)
                    
                    self.celsius_fahrenheit_button.config(text=f"{DEGREE_SYMBOL}F",command=self.fahrenheit)
                    
                    # changing location and region
                    self.location_city_region.config(text=f"{url_response['location']['name']}, {url_response['location']['region']}, {url_response['location']['country']}")
                    
                    
                    # adding weather in degree celsius
                    self.weather_show.config(text=f"{url_response['current']['temp_c']}{DEGREE_SYMBOL}C /")
                    
                    
                    # adding condition            
                    self.weather_condition.config(text=f"Condition:- {url_response['current']['condition']['text']}")
                    
                    
                    # adding the details of bluebox
                    self.windspeed.config(text=f"{url_response['current']['wind_kph']} km/hr",)
                    self.pressure.config(text=f"{url_response['current']['pressure_mb']} mb",)
                    self.humidity.config(text=f"{url_response['current']['humidity']}%",)
                    self.feels_like.config(text=f"{url_response['current']['feelslike_c']}{DEGREE_SYMBOL}C",)
                    
                    
                    air_quality = url_response['current']['air_quality']
                    if air_quality['gb-defra-index']>=1 and air_quality['gb-defra-index']<4:
                        background_color = "#80FF00"
                        self.quality.config(text="Quality:- Low",bg=background_color)
                    elif air_quality['gb-defra-index']>=4 and air_quality['gb-defra-index']<7:
                        background_color = "#F2D414"
                        self.quality.config(text="Quality:- Moderate",bg=background_color)
                    elif air_quality['gb-defra-index']>=7 and air_quality['gb-defra-index']<10:
                        background_color = "#CC0000"
                        self.quality.config(text="Quality:- High",bg=background_color)
                    elif air_quality['gb-defra-index']==10:
                        background_color = "#99004C"
                        self.quality.config(text="AQI:- Very High",bg=background_color)
                    
                    
                    self.air_quality_frame.config(bg=background_color)
                    self.aqi_co.config(text=f"CO:- {air_quality['co']}",bg=background_color)
                    self.aqi_no2.config(text=f"NO2:- {air_quality['no2']}",bg=background_color)
                    self.aqi_o3.config(text=f"O3:- {air_quality['o3']}""",bg=background_color)
                    self.aqi_so2.config(text=f"SO2:- {air_quality['so2']}",bg=background_color)
                    self.aqi_pm2_5.config(text=f"PM 2.5:- {air_quality['pm2_5']}",bg=background_color)
                    self.aqi_pm10.config(text=f"PM 10:- {air_quality['pm10']}",bg=background_color)
                    self.aqi_gb_defra_index.config(text=f"GB Defra Index:- {air_quality['gb-defra-index']}",bg=background_color)
                    
                    self.response = url_response
                
                except KeyError:
                    self.celsius_fahrenheit_button.place_forget()
                    self.location_city_region.config(text="This Location doesn't Exist")
                    self.weather_show.config(text="ERROR")
                    self.windspeed.config(text="-")
                    self.humidity.config(text="-")
                    self.feels_like.config(text="-")
                    self.pressure.config(text="-")
                    
                    self.air_quality_frame.config(bg="#C3CAC9")
                    self.aqi_co.config(text="No Data",bg="#C3CAC9")
                    self.aqi_no2.config(text="No Data",bg="#C3CAC9")
                    self.aqi_o3.config(text="No Data",bg="#C3CAC9")
                    self.aqi_so2.config(text="No Data",bg="#C3CAC9")
                    self.aqi_pm2_5.config(text="No Data",bg="#C3CAC9")
                    self.aqi_pm10.config(text="No Data",bg="#C3CAC9")
                    self.aqi_gb_defra_index.config(text="No Data",bg="#C3CAC9")
                    self.quality.config(text="No Data",bg="#C3CAC9")
                    
                    self.weather_condition.config(text="No Data")
            
            else:
                self.default_location()
        
        except Exception as e:
            self.default_location()
    
    
    def infoui(self):
        '''It's UI to enter your API Key details'''
        import webbrowser
        
        def verfiy_api():
            location = get("https://ipinfo.io/json").json()["loc"]
            check = get(f"https://api.weatherapi.com/v1/current.json?key={api_key.get()}&q={location}&aqi=no")
            
            if check.status_code==200:
                Label(self.window,text="Verified!!!!",font="Helvetica 14 bold").place(x=600,y=40)
                submit_button.config(state="normal")
                
            else:
                showerror(title="API key Issue",message="The api key you have entered is not correct or it is been disabled please check your API key??")
        
        
        def storing_api_key():
            if ".com" not in emailid.get().lower() or "@" not in emailid.get().lower(): 
                    showerror(title="Email Error",message="I think it is not a valid Email ID??")
            else:
                with open("account.dat","wb") as file:
                    info = {"email":emailid.get(),"api_key":api_key.get()}
                    
                    dump(info,file)
                self.window.destroy()
                # time.sleep(1)
                self.__init__()
                self.API_KEY = api_key.get()
                self.default_location()
                self.mainui()
    
        # GUI Icon
        information_icon = PhotoImage(file="information_icon.png")
        
        self.window.title("Information")
        self.window.iconphoto(False,information_icon)
        self.window.geometry("850x205")
        self.window.resizable(False,False)
        
        Label(self.window,text='Email ID: ',font="Helvetica 16 bold").place(x=1,y=1)
        Label(self.window,text='API Key: ',font="Helvetica 16 bold").place(x=1,y=31)
        
        
        emailid = StringVar()
        api_key = StringVar()
        
        Entry(self.window,textvariable=emailid,width=32,font="Helvetica 14 bold").place(x=100,y=2)
        Entry(self.window,textvariable=api_key,width=32,font="Helvetica 14 bold").place(x=100,y=32)
        
        Button(self.window,text="Verify API Key",font="Aerial 8 bold",command=verfiy_api).place(x=460,y=32)
        
        submit_button = Button(self.window,text="Submit",state="disabled",font="Aerial 12 bold",command=storing_api_key)
        submit_button.place(x=2,y=70)
        
        Label(self.window,text="IMPORTANT!! The API Key Should Be Of 'weatherapi.com' other than API\nkey will cause error.Go to https://www.weatherapi.com/ to get your API key.",font="Helvetica 16 bold",fg="#FF0000").place(x=0,y=120)
        
        Button(self.window,text="https://www.weatherapi.com/",font="Roboto 15 bold",fg="#004C99",border=0,
               borderwidth=0,command=lambda :webbrowser.open("https://www.weatherapi.com/")).place(x=262,y=142)
        
        self.window.mainloop()
    
    
    def celsius(self):
        '''The function to show weather in Degree Celsius if button is pressed'''
        
        len_of_weather = len(str(self.response['current']['temp_c']))+2
        if len_of_weather>6:
            self.celsius_fahrenheit_button.place(x=735,y=100)
        elif len_of_weather<6:
            self.celsius_fahrenheit_button.place(x=690,y=100)
        else:
            self.celsius_fahrenheit_button.place(x=710,y=100)
        
        self.celsius_fahrenheit_button.config(text=f"{DEGREE_SYMBOL}F",command=self.fahrenheit)
        self.weather_show.config(text=f"{self.response["current"]["temp_c"]}{DEGREE_SYMBOL}C /")
        self.feels_like.config(text=f"{self.response['current']['feelslike_c']}{DEGREE_SYMBOL}C")
    
    
    def fahrenheit(self):
        '''The function to show weather in Fahrenheit when button is pressed'''
        
        len_of_weather = len(str(self.response['current']['temp_f']))+2
        if len_of_weather>6:
            self.celsius_fahrenheit_button.place(x=725,y=100)
        elif len_of_weather<6:
            self.celsius_fahrenheit_button.place(x=695,y=100)
        else:
            self.celsius_fahrenheit_button.place(x=710,y=100)
            
        self.celsius_fahrenheit_button.config(text=f"{DEGREE_SYMBOL}C",command=self.celsius)
        self.weather_show.config(text=f"{self.response['current']['temp_f']}{DEGREE_SYMBOL}F /")
        self.feels_like.config(text=f"{self.response['current']['feelslike_f']}{DEGREE_SYMBOL}F")
    
    
    def show_time(self):
        time_am_pm = time.strftime("%I:%M %p")
        self.show_time_widget.config(text=time_am_pm)
        self.show_time_widget.after(1000,self.show_time)
        self.show_time_widget.place(x=6,y=100)
    
    
    def mainui(self):
        '''It's Main UI where you will see weather information and AQI of that particular location'''
        
        # to fetch weather and AQI of your current location
        self.default_location()
        
        self.window.title("Weather App")
        self.window.geometry("1220x505")
        self.window.resizable(False,False)
        self.window.configure(bg="#101010")
        
        # Images
        gui_icon = PhotoImage(file="icon.png")
        weather_icon = PhotoImage(file="weather_icon.png")
        search_icon = PhotoImage(file="search_icon.png")
        location_icon = PhotoImage(file="location_icon.png")
        
        # Window Icon
        self.window.iconphoto(False,gui_icon)
        
        #entry widget
        entry_widget = Entry(self.window,textvariable=self.store_location,width=24,justify="center",background="#404040",foreground="#FFFFFF",border=0,font="Consolas 25 bold")
        entry_widget.place(x=10,y=10)
        entry_widget.bind("<Return>",self.weather)
        entry_widget.focus()
        
        
        #button for search
        Button(self.window,image=search_icon,bg="#101010",borderwidth=0,border=0,command=self.weather).place(x=450,y=6)
        
        # current weather text to show after user press search button or enter
        Label(self.window,text="Current Weather",font="Helvetica 20 bold",bg="#101010",fg="#FFFFFF").place(x=6,y=60)
        
        # to show current time when press search button or enter
        self.show_time()
        
        # to show city and region
        Label(image=location_icon,bg="#101010").place(x=510,y=6)
        
        self.location_city_region.place(x=560,y=12)
        self.location_city_region.config(text=f"""{self.response["location"]["name"]}, {self.response["location"]["region"]}, {self.response["location"]["country"]}""")
        
        # showing weather icon
        Label(self.window,image=weather_icon,bg="#101010").place(x=160,y=100)
        
        # showing weather
        self.weather_show.place(x=412,y=115)
        self.weather_show.config(text=f"{self.response["current"]["temp_c"]}{DEGREE_SYMBOL}C /")
        
        # showing condition
        self.weather_condition.place(x=422,y=200)
        self.weather_condition.config(text=f"""Condition:- {self.response['current']['condition']['text']}""")
        
        # Button to switch between degree celsius and degree fahrenheit
        len_of_weather = len(str(self.response['current']['temp_f']))+2
        if len_of_weather>6:
            self.celsius_fahrenheit_button.place(x=725,y=100)
        elif len_of_weather<6:
            self.celsius_fahrenheit_button.place(x=695,y=100)
        else:
            self.celsius_fahrenheit_button.place(x=710,y=100)
        self.celsius_fahrenheit_button.config(text=f"{DEGREE_SYMBOL}F",command=self.fahrenheit)
        
        
        # To show Wind Speed, Humidity, Description and Pressure
        self.below_details.place(x=-10,y=390)
        
        Label(self.below_details,text="""WIND SPEED                                HUMIDITY                                FEELS LIKE                                PRESSURE""",font="Default 18 bold",fg="#FFFFFF",bg="#0066CC",border=0,borderwidth=0).place(x=10,y=10)
        
        self.windspeed.config(text=f"""{self.response['current']['wind_kph']} km/hr""")
        self.windspeed.place(x=15,y=70)
        
        self.humidity.config(text=f"""{self.response['current']['humidity']}%""")
        self.humidity.place(x=415,y=70)
        
        self.feels_like.config(text=f"""{self.response['current']['feelslike_c']}{DEGREE_SYMBOL}C""")
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
    
    
    def main_execution(self):
        try:
            with open("account.dat","rb") as file:
                self.API_KEY = load(file)['api_key']
            self.mainui()
        except:
            self.infoui()
    
    
if __name__ == '__main__':
    app = WeatherApp()
    app.main_execution()

