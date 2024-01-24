
from tkinter import Tk,Button,Entry,StringVar,PhotoImage,Label
from json import load
from urllib.request import urlopen
from random import shuffle,randint
from os import getcwd,getenv,listdir
from dotenv import load_dotenv
from multiprocessing import Process

load_dotenv()

def weather():
    if len(weth.get())!=0:
        try:
            location = str(weth.get())
            location = location.replace(" ","%20")
            url = urlopen(f"https://api.weatherapi.com/v1/current.json?key={getenv('api_key')}&q={location}&aqi=no")
            location_weather = load(url)
            del url 
            del location
            location_weather = f"""Temperature:- {location_weather["current"]["temp_c"]}\u00b0C/{location_weather["current"]["temp_f"]}\u00b0F\nRegion:- {location_weather["location"]["region"]}\nCity:- {location_weather["location"]["name"]}\nCondition:- {location_weather["current"]["condition"]["text"]}"""
            
            
            showing_weather.config(text=location_weather)
            showing_weather.after(500,weather)
        except:
            showing_weather.config(text="This Location doesn't Exist Please\ncheck the spelling.")
    else:
        location = urlopen("https://ipinfo.io/json")
        location = str(load(location)["city"])
        url = urlopen(f"https://api.weatherapi.com/v1/current.json?key={getenv('api_key')}&q={location}&aqi=no")
        del location
        return load(url)


def main():
    root = Tk()
    root.maxsize(627,427)

    root.title("Weather")
    # setting icon
    icon = PhotoImage(file="/media/newdriveee/programs/githubb/Tkinter-Weather-GUI/png/icon.png")

    root.iconphoto(True,icon)


    # Making a background image
    # # Making a list of background images

    image_list = [image for image in listdir("/media/newdriveee/programs/githubb/Tkinter-Weather-GUI/png")]

    image_list.remove("icon.png")
    shuffle(image_list)


    image0 = PhotoImage(file=f"{getcwd()}/png/{image_list[randint(0,len(image_list)-1)]}")


    def change_background_image():
        new_image = PhotoImage(file=f"{getcwd()}/png/{image_list[randint(0, len(image_list)-1)]}")
        
        showing_image.config(image=new_image)
        showing_image.image = new_image
        showing_image.after(60000,change_background_image)


    showing_image = Label(root,image=image0)
    showing_image.pack()


    change_background_image()
    
    
    # Making a entry to enter a city
    # # Entry
    global weth
    weth = StringVar()
    Entry(root,textvariable=weth,width=40).place(x=150,y=0)
    
    
    # # Making Search Button
    Button(root,text="SUBMIT!!",font="Aerial 7 bold",command=weather).place(x=430,y=0)


    # Making Exit Button
    Button(root,text="EXIT!!",font="Aerial 7 bold",command=exit).place(x=540,y=0)

    # Showing wheather
    global showing_weather
    showing_weather = Label(root,text=f"""Temperature:- {weather()["current"]["temp_c"]}\u00b0C/{weather()["current"]["temp_f"]}\u00b0F\nRegion:- {weather()["location"]["region"]}\nCity:- {weather()["location"]["name"]}\nCondition:- {weather()["current"]["condition"]["text"]}""",borderwidth=0,font="Aerial 12 bold",border=0)


    showing_weather.place(x=210,y=160)


    root.mainloop()


if __name__ == "__main__":
    Process(target=main).start()