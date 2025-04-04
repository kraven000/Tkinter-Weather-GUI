# from tkinter import Tk,Label,Entry,Button,Frame,PhotoImage,StringVar
from customtkinter import CTk,CTkLabel,CTkEntry,CTkButton,CTkFrame,CTkImage,StringVar
from PIL import Image, ImageTk
from tkinter.messagebox import showerror
from requests import get
from pickle import load,dump
import time


DEGREE_SYMBOL = u"\u00b0"

class WeatherApp:
    def __init__(self):
        
        self.API_KEY = None
        self.response = self.default_location()
        self.window = CTk()
        self.store_location = StringVar()
        self.weather_show = CTkLabel(self.window,font=("Helvetica",80),text_color="#FFFFFF",fg_color="#202020")
        self.location_city_region = CTkLabel(self.window,font=("Helvetica",20),fg_color="#202020",text_color="#FFFFFF")
        self.weather_condition = CTkLabel(self.window,font=("Consolas",16),fg_color="#202020",text_color="#FFFFFF")
        self.below_details = CTkFrame(self.window,fg_color="#0066CC",width=1300,height=120)
        self.windspeed = CTkLabel(self.below_details,fg_color="#0066CC",text_color="#202020",font=("default",30))
        self.humidity = CTkLabel(self.below_details,fg_color="#0066CC",text_color="#202020",font=("default",30))
        self.feels_like = CTkLabel(self.below_details,fg_color="#0066CC",text_color="#202020",font=("default",30))
        self.pressure = CTkLabel(self.below_details,fg_color="#0066CC",text_color="#202020",font=("default",30))
        self.air_quality_frame = CTkFrame(self.window,width=300,height=280)
        self.aqi_co = CTkLabel(self.air_quality_frame,font=("Roboto",22),text_color="#FFFFFF")
        self.aqi_no2 = CTkLabel(self.air_quality_frame,font=("Roboto",22),text_color="#FFFFFF")
        self.aqi_o3 = CTkLabel(self.air_quality_frame,font=("Roboto",22),text_color="#FFFFFF")
        self.aqi_so2 = CTkLabel(self.air_quality_frame,font=("Roboto",22),text_color="#FFFFFF")
        self.aqi_pm2_5 = CTkLabel(self.air_quality_frame,font=("Roboto",22),text_color="#FFFFFF")
        self.aqi_pm10 = CTkLabel(self.air_quality_frame,font=("Roboto",22),text_color="#FFFFFF")
        self.aqi_gb_defra_index = CTkLabel(self.air_quality_frame,font=("Roboto",22),text_color="#FFFFFF")
        self.celsius_fahrenheit_button = CTkButton(self.window,text=f"{DEGREE_SYMBOL}F",
                                                font=("Helvetica",80),text_color="#FFFFFF",fg_color="#202020",
                                                width=2,command=self.fahrenheit)
        self.quality = CTkLabel(self.air_quality_frame,font=("Roboto",20),text_color="#FFFFFF")
        
        self.show_time_widget = CTkLabel(self.window,text="",font=("Helvetica",20),fg_color="#202020",
                                      text_color="#FFFFFF")
    
    
    def default_location(self):
        location = get(("https://ipinfo.io/json")).json()
        location = location["loc"]
        # weather
        # url = get(f"https://api.weatherapi.com/v1/current.json?key={self.API_KEY}&q={location}&aqi=yes").json()
        
        with open('temp.json', 'r') as file:
            import json
            data = json.load(file)
        self.response = data
    
    
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
                        self.celsius_fahrenheit_button.place(x=721,y=175)
                    elif len_of_weather<6:
                        self.celsius_fahrenheit_button.place(x=657,y=175)
                    else:
                        self.celsius_fahrenheit_button.place(x=705,y=175)
                    
                    self.celsius_fahrenheit_button.configure(text=f"{DEGREE_SYMBOL}F",command=self.fahrenheit)
                    
                    # changing location and region
                    self.location_city_region.configure(text=f"{url_response['location']['name']}, {url_response['location']['region']}, {url_response['location']['country']}")
                    
                    
                    # adding weather in degree celsius
                    self.weather_show.configure(text=f"{url_response['current']['temp_c']}{DEGREE_SYMBOL}C /")
                    
                    
                    # adding condition            
                    self.weather_condition.configure(text=f"Condition:- {url_response['current']['condition']['text']}")
                    
                    
                    # adding the details of bluebox
                    self.windspeed.configure(text=f"WIND SPEED\n\n{url_response['current']['wind_kph']} km/hr",)
                    self.pressure.configure(text=f"PRESSURE\n\n{url_response['current']['pressure_mb']} mb",)
                    self.humidity.configure(text=f"HUMIDITY\n\n{url_response['current']['humidity']}%",)
                    self.feels_like.configure(text=f"FEELS LIKE\n\n{url_response['current']['feelslike_c']}{DEGREE_SYMBOL}C",)
                    
                    
                    air_quality = url_response['current']['air_quality']
                    
                    background_color = None
                    quality_text = None
                    
                    if air_quality['gb-defra-index']>=1 and air_quality['gb-defra-index']<4:
                        background_color = "#009900"
                        quality_text = "Low"
                    elif air_quality['gb-defra-index']>=4 and air_quality['gb-defra-index']<7:
                        background_color = "#FF9B00"
                        quality_text = "Moderate"
                    elif air_quality['gb-defra-index']>=7 and air_quality['gb-defra-index']<10:
                        background_color = "#FF0000"
                        quality_text = "High"
                    elif air_quality['gb-defra-index']==10:
                        background_color = "#800080"
                        quality_text = "Very High"
                    
                    self.quality.configure(text=f"AQI:- {quality_text}",fg_color=background_color)
                    
                    self.air_quality_frame.configure(fg_color=background_color,)
                    self.aqi_co.configure(text=f"CO:- {air_quality['co']}",fg_color=background_color)
                    self.aqi_no2.configure(text=f"NO2:- {air_quality['no2']}",fg_color=background_color)
                    self.aqi_o3.configure(text=f"O3:- {air_quality['o3']}""",fg_color=background_color)
                    self.aqi_so2.configure(text=f"SO2:- {air_quality['so2']}",fg_color=background_color)
                    self.aqi_pm2_5.configure(text=f"PM 2.5:- {air_quality['pm2_5']}",fg_color=background_color)
                    self.aqi_pm10.configure(text=f"PM 10:- {air_quality['pm10']}",fg_color=background_color)
                    self.aqi_gb_defra_index.configure(text=f"GB Defra Index:- {air_quality['gb-defra-index']}",
                                                   fg_color=background_color)
                    
                    self.response = url_response
                
                except KeyError:
                    self.celsius_fahrenheit_button.place_forget()
                    self.location_city_region.configure(text="This Location doesn't Exist")
                    self.weather_show.configure(text="ERROR")
                    self.windspeed.configure(text="-")
                    self.humidity.configure(text="-")
                    self.feels_like.configure(text="-")
                    self.pressure.configure(text="-")
                    
                    self.air_quality_frame.configure(fg_color="#C3CAC9")
                    self.aqi_co.configure(text="No Data",fg_color="#C3CAC9")
                    self.aqi_no2.configure(text="No Data",fg_color="#C3CAC9")
                    self.aqi_o3.configure(text="No Data",fg_color="#C3CAC9")
                    self.aqi_so2.configure(text="No Data",fg_color="#C3CAC9")
                    self.aqi_pm2_5.configure(text="No Data",fg_color="#C3CAC9")
                    self.aqi_pm10.configure(text="No Data",fg_color="#C3CAC9")
                    self.aqi_gb_defra_index.configure(text="No Data",fg_color="#C3CAC9")
                    self.quality.configure(text="No Data",fg_color="#C3CAC9")
                    
                    self.weather_condition.configure(text="No Data")
            
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
                CTkLabel(self.window,text="Verified!!!!",font=("Helvetica",14)).place(x=600,y=40)
                submit_button.configure(state="normal")
                
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
        # information_icon = PhotoImage(file="information_icon.png")
        information_icon = ImageTk.PhotoImage(Image.open("information_icon.png"))
        
        self.window.title("Information")
        self.window.wm_iconbitmap()
        self.window.iconphoto(False,information_icon)
        self.window.geometry("850x205")
        self.window.resizable(False,False)
        
        CTkLabel(self.window,text='Email ID: ',font=("Helvetica",16)).place(x=1,y=1)
        CTkLabel(self.window,text='API Key: ',font=("Helvetica",16)).place(x=1,y=31)
        
        
        emailid = StringVar()
        api_key = StringVar()
        
        CTkEntry(self.window,textvariable=emailid,width=32,font=("Helvetica",14)).place(x=100,y=2)
        CTkEntry(self.window,textvariable=api_key,width=32,font=("Helvetica",14)).place(x=100,y=32)
        
        CTkButton(self.window,text="Verify API Key",font=("Aerial",8),command=verfiy_api).place(x=460,y=32)
        
        submit_button = CTkButton(self.window,text="Submit",state="disabled",font=("Aerial",12),command=storing_api_key)
        submit_button.place(x=2,y=70)
        
        CTkLabel(self.window,text="IMPORTANT!! The API Key Should Be Of 'weatherapi.com' other than API\nkey will cause error.Go to https://www.weatherapi.com/ to get your API key.",
                 font=("Helvetica",16),text_color="#FF0000").place(x=0,y=120)
        
        CTkButton(self.window,text="https://www.weatherapi.com/",font=("Roboto",15),text_color="#004C99",
                  command=lambda :webbrowser.open("https://www.weatherapi.com/")).place(x=262,y=142)
        
        self.window.mainloop()
    
    
    def celsius(self):
        '''The function to show weather in Degree Celsius if button is pressed'''
        
        len_of_weather = len(str(self.response['current']['temp_c']))+2
        if len_of_weather>6:
            self.celsius_fahrenheit_button.place(x=721,y=175)
        elif len_of_weather<6:
            self.celsius_fahrenheit_button.place(x=657,y=175)
        else:
            self.celsius_fahrenheit_button.place(x=705,y=175)
        
        self.celsius_fahrenheit_button.configure(text=f"{DEGREE_SYMBOL}F",command=self.fahrenheit)
        self.weather_show.configure(text=f"{self.response["current"]["temp_c"]}{DEGREE_SYMBOL}C /")
        self.feels_like.configure(text=f"FEELS LIKE\n\n{self.response['current']['feelslike_c']}{DEGREE_SYMBOL}C")
    
    
    def fahrenheit(self):
        '''The function to show weather in Fahrenheit when button is pressed'''
        
        len_of_weather = len(str(self.response['current']['temp_f']))+2
        if len_of_weather>6:
            self.celsius_fahrenheit_button.place(x=721,y=175)
        elif len_of_weather<6:
            self.celsius_fahrenheit_button.place(x=657,y=175)
        else:
            self.celsius_fahrenheit_button.place(x=705,y=175)
            
        self.celsius_fahrenheit_button.configure(text=f"{DEGREE_SYMBOL}C",command=self.celsius)
        self.weather_show.configure(text=f"{self.response['current']['temp_f']}{DEGREE_SYMBOL}F /")
        self.feels_like.configure(text=f"FEELS LIKE\n\n{self.response['current']['feelslike_f']}{DEGREE_SYMBOL}F")
    
    
    def show_time(self):
        time_am_pm = time.strftime("%I:%M %p")
        self.show_time_widget.configure(text=time_am_pm)
        self.show_time_widget.after(1000,self.show_time)
        self.show_time_widget.place(x=6,y=100)
    
    
    def mainui(self):
        '''It's Main UI where you will see weather information and AQI of that particular location'''
        
        # to fetch weather and AQI of your current location
        self.default_location()
        
        self.window.title("Weather App")
        self.window.geometry("1220x505")
        self.window.resizable(False,False)
        self.window.configure(fg_color="#202020")
        
        # Images
        gui_icon = ImageTk.PhotoImage((Image.open("icon.png")))
        weather_icon = CTkImage(Image.open("weather_icon.png"),size=(250,250))
        search_icon = CTkImage(Image.open("search_icon.png"),size=(46,46))
        location_icon = CTkImage(Image.open("location_icon.png"),size=(46,46))
        
        # Window Icon
        self.window.wm_iconbitmap()
        self.window.iconphoto(False,gui_icon)
        
        #entry widget
        entry_widget = CTkEntry(self.window,textvariable=self.store_location,width=400,justify="center",
                                fg_color="#404040",text_color="#FFFFFF",font=("Consolas",30))
        entry_widget.place(x=10,y=10)
        entry_widget.bind("<Return>",self.weather)
        entry_widget.focus()
        
        
        #button for search
        CTkButton(self.window,text="",image=search_icon,fg_color="#202020",bg_color="transparent",width=50,
                  command=self.weather).place(x=410,y=6)
        
        # current weather text to show after user press search button or enter
        CTkLabel(self.window,text="Current Weather",font=("Helvetica",20),fg_color="#202020",
                 text_color="#FFFFFF").place(x=6,y=65)
        
        # to show current time when press search button or enter
        self.show_time()
        
        # to show city and region
        self.location_city_region.place(x=480,y=10)
        self.location_city_region.configure(text=f"""{self.response["location"]["name"]}, {self.response["location"]["region"]}, {self.response["location"]["country"]}""",
                                            image=location_icon,compound="left")
        
        # showing weather
        self.weather_show.place(x=127,y=100)
        self.weather_show.configure(text=f"{self.response["current"]["temp_c"]}{DEGREE_SYMBOL}C /",
                                    image=weather_icon,compound="left")
        
        # showing condition
        self.weather_condition.place(x=380,y=260)
        self.weather_condition.configure(text=f"""Condition:- {self.response['current']['condition']['text']}""")
        
        # Button to switch between degree celsius and degree fahrenheit
        len_of_weather = len(str(self.response['current']['temp_f']))+2
        if len_of_weather>6:
            self.celsius_fahrenheit_button.place(x=721,y=175)
        elif len_of_weather<6:
            self.celsius_fahrenheit_button.place(x=657,y=175)
        else:
            self.celsius_fahrenheit_button.place(x=705,y=175)
        self.celsius_fahrenheit_button.configure(text=f"{DEGREE_SYMBOL}F",command=self.fahrenheit)
        
        
        # To show Wind Speed, Humidity, Description and Pressure
        self.below_details.pack(anchor="s",expand=True)
        self.below_details.pack_propagate(False)
        
        
        self.windspeed.configure(text=f"""WIND SPEED\n\n{self.response['current']['wind_kph']} km/hr""")
        self.windspeed.pack(side="left",padx=15,pady=0)
        
        self.humidity.configure(text=f"""HUMIDITY\n\n{self.response['current']['humidity']}%""")
        self.humidity.pack(side="left",padx=120,pady=0)
        
        self.feels_like.configure(text=f"""FEELS LIKE\n\n{self.response['current']['feelslike_c']}{DEGREE_SYMBOL}C""")
        self.feels_like.pack(side="left",padx=120,pady=0)
        
        self.pressure.configure(text=f"""PRESSURE\n\n{self.response['current']['pressure_mb']} mb""")
        self.pressure.pack(side="left",padx=15,pady=0)
        
        
        # To show air quality
        air_quality_index = self.response["current"]["air_quality"]["gb-defra-index"]
        quality_text = None
        background_color = None
        if air_quality_index>=1 and air_quality_index<4:
            background_color = "#009900"
            quality_text = "AQI:- Low"
            
        elif air_quality_index>=4 and air_quality_index<7:
            background_color = "#FF9B00"
            quality_text = "AQI:- Moderate"
            
        elif air_quality_index>=7 and air_quality_index<10:
            background_color = "#FF0000"
            quality_text = "AQI:- High"
            
        elif air_quality_index==10:
            background_color = "#800080"
            quality_text = "AQI:- Very High"
            
        
        self.air_quality_frame.configure(fg_color=background_color)
        self.air_quality_frame.place(x=850,y=53)
        
        
        self.aqi_co.configure(text=f"""CO:- {self.response["current"]["air_quality"]["co"]}""",fg_color=background_color)
        self.aqi_co.place(x=0,y=5)
        
        self.aqi_no2.configure(text=f"""NO2:- {self.response["current"]["air_quality"]["no2"]}""",fg_color=background_color)
        self.aqi_no2.place(x=0,y=38)
        
        
        self.aqi_o3.place(x=0,y=71)
        self.aqi_o3.configure(text=f"""O3:- {self.response["current"]["air_quality"]["o3"]}""",fg_color=background_color)
        
        self.aqi_so2.place(x=0,y=104)
        self.aqi_so2.configure(text=f"""SO2:- {self.response["current"]["air_quality"]["so2"]}""",fg_color=background_color)
        
        self.aqi_pm2_5.place(x=0,y=137)
        self.aqi_pm2_5.configure(text=f"""PM 2.5:- {self.response["current"]["air_quality"]["pm2_5"]}""",fg_color=background_color)
        
        self.aqi_pm10.place(x=0,y=170)
        self.aqi_pm10.configure(text=f"""PM 10:- {self.response["current"]["air_quality"]["pm10"]}""",fg_color=background_color)
        
        self.aqi_gb_defra_index.place(x=0,y=203)
        self.aqi_gb_defra_index.configure(text=f"""GB Defra Index:- {self.response["current"]["air_quality"]["gb-defra-index"]}""",fg_color=background_color)
        
        self.quality.place(x=0,y=236)
        self.quality.configure(text=quality_text,fg_color=background_color)
        
        self.window.mainloop()
    
    
    def main_execution(self):
        try:
            with open("account.dat","rb") as file:
                self.API_KEY = load(file)['api_key']
            self.mainui()
        except FileNotFoundError:
            self.infoui()
    
    
if __name__ == '__main__':
    app = WeatherApp()
    app.main_execution()

