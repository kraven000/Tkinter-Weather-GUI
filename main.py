
from tkinter import Tk,Button,Entry,StringVar,PhotoImage,Label
from json import load
from urllib.request import urlopen
from random import shuffle,randint
from os import getcwd,getenv
from dotenv import load_dotenv


def default_weather():
    load_dotenv()
    
    location = urlopen("https://ipinfo.io/json")
    location = str(load(location)["city"])
    url = urlopen(f"https://api.weatherapi.com/v1/current.json?key={getenv('api_key')}&q={location}&aqi=yes")
    return load(url)


def change_weather():
    load_dotenv()
    if len(weth.get())!=0:
        location = str(weth.get())
        location = location.replace(" ","%20")
        url = urlopen(f"https://api.weatherapi.com/v1/current.json?key={getenv('api_key')}&q={location}&aqi=yes")
        location_weather = load(url)
        location_weather = f"""Temperature:- {location_weather["current"]["temp_c"]}{degree}C/{location_weather["current"]["temp_f"]}{degree}F\nRegion:- {location_weather["location"]["region"]}\nCity:- {location_weather["location"]["name"]}\nCondition:- {location_weather["current"]["condition"]["text"]}"""
        
        del url 
        del location
        
        si.config(text=location_weather)
        si.after(1000,change_weather)


root = Tk()
root.geometry("627x427")
root.title("Weather")

# Making a background image
# # Making a list of background images
image_list = ['sunset-3352685_640.png', 'autumn-3010000_640.png', 'heaven-4757785_640.png', 'sky-2076878_640.png', 'milky-way-3602131_640.png']

shuffle(image_list)

image0 = PhotoImage(file=f"{getcwd()}/png/{image_list[randint(0,len(image_list)-1)]}")

Label(root,image=image0).pack()


# Making a entry to enter a city
# # Entry
weth = StringVar()
Entry(root,textvariable=weth,width=30).place(x=200,y=0)

# # Making Search Button
Button(root,text="SUBMIT!!",font="Aerial 5 bold",command=change_weather).place(x=430,y=0)

# Showing wheather
# Degree Symbol
degree = u"\u00b0"
si = Label(root,text=f"""Temperature:- {default_weather()["current"]["temp_c"]}{degree}C/{default_weather()["current"]["temp_f"]}{degree}F\nRegion:- {default_weather()["location"]["region"]}\nCity:- {default_weather()["location"]["name"]}\nCondition:- {default_weather()["current"]["condition"]["text"]}""",borderwidth=0,font="Aerial 12 bold",border=0)


si.place(x=210,y=160)


root.mainloop()