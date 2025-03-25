from tkinter import *
import tkinter as tk
from datetime import datetime
import requests
from tkinter import messagebox

class Weather:

    def detect_location(self):
        try:
            response = requests.get("http://ip-api.com/json/").json()
            if response['status'] == 'success':
                city = response['city']
                self.loc.delete(1.0, END)
                self.loc.insert(END, city)
                self.weather_report()
            else:
                raise Exception("Location Detection Failed")
        except Exception:
            messagebox.showwarning("Warning", "Failed to Detect Location! Please Enter Manually.")

    def weather_report(self):
        self.cityname = self.loc.get(1.0, END).strip()
        if not self.cityname:
            messagebox.showerror("Error", "Please enter a location!")
            return

        self.url = "http://api.openweathermap.org/data/2.5/weather?q="
        self.api_key = 'b0fb61118ce54f16498765638b5fdfb8'
        self.data = requests.get(self.url + self.cityname + '&appid=' + self.api_key).json()

        if self.data['cod'] == '404':
            messagebox.showerror('Error', 'City Not Found !!')
        else:
            self.location['text'] = self.data['name'] + ", " + self.data['sys']['country']
            self.c = int(self.data['main']['temp_max'] - 273.15)
            self.f = self.c * 9 / 5 + 32
            self.weather['text'] = f"{self.data['weather'][0]['main']}"
            self.weather['font'] = ('Arial', 20, 'bold')
            self.temperature['text'] = f'{self.c}°C \n {self.f}°F'
            self.humidity['text'] = f"Humidity: {self.data['main']['humidity']}%"
            self.pressure['text'] = f"Pressure: {self.data['main']['pressure']} hPa"

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('700x400')
        self.root.title("Weather Application")
        self.root.configure(bg="#F0F8FF")

        # Header section with date and title
        self.header_frame = Frame(self.root, bg="#1F3A93", height=50)
        self.header_frame.pack(fill=X)
        self.heading = Label(self.header_frame, text="Weather Report", font=('Arial', 16, 'bold'), fg="white", bg="#1F3A93")
        self.heading.pack(pady=10)
        self.date = Label(self.header_frame, text=datetime.now().date(), fg="white", bg="#1F3A93", font=('Arial', 12))
        self.date.place(x=600, y=10)

        # Input section for entering city/country name
        self.input_frame = Frame(self.root, bg="#F0F8FF")
        self.input_frame.pack(pady=20)
        Label(self.input_frame, text="Enter City or Country Name:", font=('Arial', 12, 'bold'), bg="#F0F8FF").grid(row=0, column=0, padx=10, pady=5)
        self.loc = Text(self.input_frame, width=25, height=1, font=('Arial', 12))
        self.loc.grid(row=0, column=1, padx=10)
        self.button = Button(self.input_frame, text="Search", bg="#1F3A93", fg="white", font=('Arial', 12), command=self.weather_report)
        self.button.grid(row=0, column=2, padx=10)

        # Output section for displaying weather details
        self.output_frame = Frame(self.root, bg="#F0F8FF")
        self.output_frame.pack(pady=10)

        self.location = Label(self.output_frame, text="Location: NA", font=('Arial', 14, 'bold'), bg="#F0F8FF", fg="#1F3A93")
        self.location.grid(row=0, column=0, columnspan=3, pady=5)

        # Built-in emoji-style icons for Weather Info (no PNGs needed)
        self.weather_icon = Label(self.output_frame, text="☁️", font=('Arial', 40), bg="#F0F8FF")
        self.weather_icon.grid(row=1, column=0, padx=10)
        self.weather = Label(self.output_frame, text="Weather: NA", font=('Arial', 12), bg="#F0F8FF")
        self.weather.grid(row=2, column=0, padx=10)

        self.temp_icon = Label(self.output_frame, text="🌡️", font=('Arial', 40), bg="#F0F8FF")
        self.temp_icon.grid(row=1, column=1, padx=10)
        self.temperature = Label(self.output_frame, text="Temperature: NA", font=('Arial', 12), bg="#F0F8FF")
        self.temperature.grid(row=2, column=1, padx=10)

        self.humidity_icon = Label(self.output_frame, text="💧", font=('Arial', 40), bg="#F0F8FF")
        self.humidity_icon.grid(row=1, column=2, padx=10)
        self.humidity = Label(self.output_frame, text="Humidity: NA", font=('Arial', 12), bg="#F0F8FF")
        self.humidity.grid(row=2, column=2, padx=10)

        self.pressure = Label(self.output_frame, text="Pressure: NA", font=('Arial', 12), bg="#F0F8FF")
        self.pressure.grid(row=3, column=0, columnspan=3, pady=5)

        # Automatically detect user's location on app launch
        self.root.after(1000, self.detect_location)  # Detect after a short delay
        self.root.mainloop()


if __name__ == '__main__':
    Weather()
