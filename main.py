from tkinter import Tk,Label,Entry,Button,Frame,PhotoImage,StringVar
from time import strftime
from requests import get
from os import getenv
from dotenv import load_dotenv


load_dotenv()
time = strftime("%I:%M %p")


def weather(events=None):
    if len(store_area.get()) != 0:
        try:
            # Adding time and 'Current Weather' text
            time_text.config(text=f"{time} ")
            current_weather_text.config(text="Current Weather")
            
            # editing location to make it fit for url
            location = str(store_area.get()).strip().lower()
            location = location.replace(" ", "%20")
            
            # json file of weather
            url_response = get(url=f"https://api.weatherapi.com/v1/current.json?key={getenv('api_key')}&q={location}&aqi=no").json()
            del location
            
            # degree symbol
            degree_symbol = u"\u00b0"
            
            # changing location and region
            location_city_region.config(text=f"""{url_response["location"]["name"]}, {url_response["location"]["region"]}, {url_response["location"]["country"]}""")
            
            # adding weather in degree celsius
            weather_show.config(text=f"""{url_response["current"]["temp_c"]}{degree_symbol}C /""",font="Helvetica 60 bold",bg="#101010",fg="#FFFFFF")
            
            # adding condition            
            weather_condition.config(text=f"""{url_response["current"]["condition"]["text"]}|Feels Like:- {url_response["current"]["feelslike_c"]}{degree_symbol}C""",font="Consolas 12 bold",bg="#101010",fg="#FFFFFF")
            
            if len(str(url_response["current"]["temp_c"]))==3:
                celsius_fahrenhiet_button.place(x=680,y=110)
            else:
                celsius_fahrenhiet_button.place(x=705,y=110)
            
            
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
            return url_response
        
        except Exception as e:
            print(e)
            weather_show.config(text="This Location doesn't Exist",font="Helvetica 14 bold")
    else:
        # taking location through ipinfo
        location = get(("https://ipinfo.io/json")).json()
        location = location["city"]
        
        # weather
        url = get(f"https://api.weatherapi.com/v1/current.json?key={getenv('api_key')}&q={location}&aqi=no").json()
        del location
        return url


def celsius():
    '''The function to show weather in Degree Celsius if button is pressed'''
    
    response = weather()
    
    degree_symbol = u"\u00b0"
    
    celsius_fahrenhiet_button.config(text=f"{degree_symbol}F")
    
    if len(str(response["current"]["temp_c"]))==3:
        celsius_fahrenhiet_button.place(x=680,y=110)
    else:
        celsius_fahrenhiet_button.place(x=705,y=110)
    
    celsius_fahrenhiet_button.config(command=fahrenhiet,bg="#101010",fg="#FFFFFF")
    
    weather_show.config(text=f"""{response["current"]["temp_c"]}{degree_symbol}C /""",font="Helvetica 60 bold",bg="#101010",fg="#FFFFFF")
    weather_condition.config(text=f"""{response["current"]["condition"]["text"]}|Feels Like:- {response["current"]["feelslike_c"]}{degree_symbol}C""",font="Consolas 14 bold",bg="#101010",fg="#FFFFFF")


def fahrenhiet():
    '''The function to show weather in Fahrenhiet when button is pressed'''
    
    response = weather()
    
    degree_symbol = u"\u00b0"
    
    celsius_fahrenhiet_button.config(text=f"{degree_symbol}C")
    
    if len(str(response["current"]["temp_f"]))==5:
        celsius_fahrenhiet_button.place(x=750,y=110)
    else:
        celsius_fahrenhiet_button.place(x=705,y=110)
    
    celsius_fahrenhiet_button.config(command=celsius,bg='#101010',fg="#FFFFFF")
    
    weather_show.config(text=f"""{response["current"]["temp_f"]}{degree_symbol}F /""",font="Helvetica 60 bold",bg="#101010",fg="#FFFFFF")
    weather_condition.config(text=f"""{response["current"]["condition"]["text"]}|Feels Like:- {response["current"]["feelslike_f"]}{degree_symbol}F""",font="Consolas 14 bold",bg="#101010",fg="#FFFFFF")


def main():
    
    global time_text, current_weather_text, weather_show, store_area, weather_condition, detailed_desc, windspeed, condition, pressure, humidity, celsius_fahrenhiet_button, weather_show,location_city_region
    
    
    # root.iconphoto(True,icon)
    root = Tk()
    root.title("Weather App")
    root.geometry("1000x505")
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
    default_response = weather()
    
    
    #button for search
    Button(root,image=search_icon,bg="#101010",borderwidth=0,border=0,command=weather).place(x=500,y=6)
    
    # current weather text to show after user press search button or enter
    current_weather_text = Label(root,text="",font="Helvetica 20 bold",bg="#101010",fg="#FFFFFF")
    current_weather_text.place(x=6,y=60)
    
    # to show current time when press search button or enter
    time_text = Label(root,text=f"",font="Helvetica 20 bold",bg="#101010",fg="#FFFFFF")
    time_text.place(x=6,y=100)
    
    # to show city and region
    Label(image=location_icon,bg="#101010").place(x=560,y=6)
    
    location_city_region = Label(root,text=f"""{default_response["location"]["name"]}, {default_response["location"]["region"]}, {default_response["location"]["country"]}""",font="Helvetica 16 bold",bg="#101010",fg="#FFFFFF")
    location_city_region.place(x=605,y=12)
    
    # showing weather icon
    Label(root,image=weather_icon,bg="#101010").place(x=160,y=100)
    
    # showing weather
    degree_symbol = u"\u00b0"
    weather_show = Label(root,text=f"""{default_response["current"]["temp_c"]}{degree_symbol}C /""",font="Helvetica 60 bold",fg="#FFFFFF",bg="#101010")
    weather_show.place(x=412,y=115)
    
    # showing condition
    weather_condition = Label(root,text=f"""{default_response["current"]["condition"]["text"]}|Feels Like:- {default_response["current"]["feelslike_c"]}{degree_symbol}C""",font="Consolas 12 bold",bg="#101010",fg="#FFFFFF")
    weather_condition.place(x=422,y=200)
    
    # Button to switch between degree celsius and degree fahrenheit
    celsius_fahrenhiet_button = Button(root,text=f"{degree_symbol}F",font="Helvetica 60 bold",fg="#FFFFFF",bg="#101010",border=0,borderwidth=0,command=fahrenhiet)
    if len(str(default_response["current"]["temp_c"]))==3:
        celsius_fahrenhiet_button.place(x=680,y=110)
    else:
        celsius_fahrenhiet_button.place(x=705,y=110)
    
    
    # Frame for Background
    frame = Frame(root,bg="#0066CC",width=1100,height=120)
    frame.place(x=-10,y=390)
    
    # To show Wind Speed, HUmidity, Description and Pressure
    Label(root,text="WIND SPEED         HUMIDITY          DESCRIPTION              PRESSURE",font="Default 18 bold",fg="#FFFFFF",bg="#0066CC",border=0,borderwidth=0).place(x=0,y=400)
    
    windspeed = Label(root,text=f"""{default_response["current"]["wind_kph"]} km/hr""",bg="#0066CC",fg="#202020",font="default 16 bold")
    windspeed.place(x=5,y=450)
    
    humidity = Label(root,text=f"""{default_response["current"]["humidity"]}%""",bg="#0066CC",fg="#202020",font="default 16 bold")
    humidity.place(x=280,y=450)
    
    condition = Label(root,text=f"""{default_response["current"]["condition"]["text"]}""",bg="#0066CC",fg="#202020",font="default 16 bold")
    condition.place(x=455,y=450)
    
    pressure = Label(root,text=f"""{default_response["current"]["pressure_mb"]} mb""",bg="#0066CC",fg="#202020",font="default 16 bold")
    pressure.place(x=760,y=450)
    
    
    root.mainloop()


if __name__ == "__main__":
    main()