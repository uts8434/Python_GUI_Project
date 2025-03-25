from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import requests
from deep_translator import GoogleTranslator
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 90)
engine.setProperty('volume', 0.7)

root = tk.Tk()
root.title('Enhanced Dictionary & Translator')

root.geometry('750x400')
root['bg'] = '#F8F8F8'  # Subtle background for a cleaner look

# Function Definitions
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def speak_input_text():
    input_text = entry.get().strip()
    if input_text:
        speak_text(input_text)
    else:
        messagebox.showinfo("Info", "Please enter a word or sentence to speak.")

def speak_output_text():
    output_text = output.get("1.0", "end").strip()
    selected_language = language_combo.get()
    if output_text:
        if selected_language == 'English-to-English':
            speak_text(output_text)
        else:
            messagebox.showinfo("Info", "Hindi text can't be spoken.")
    else:
        messagebox.showinfo("Info", "No text to speak. Please search for a word or sentence first.")

def get_meaning_or_translation():
    input_text = entry.get().strip()
    selected_language = language_combo.get()

    if input_text == "":
        messagebox.showerror('Dictionary', 'Please write a word or sentence')
        return

    output.delete('1.0', END)

    if selected_option.get() == "Word":
        if selected_language == 'English-to-English':
            try:
                response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{input_text}")
                if response.status_code == 200:
                    data = response.json()
                    meaning = data[0]['meanings'][0]['definitions'][0]['definition']
                    output.insert('end', f" {meaning}\n")
                else:
                    output.insert('end', f"No meaning found for '{input_text}'\n")
            except Exception as e:
                messagebox.showerror('Error', f"Could not fetch the meaning. {e}")

        elif selected_language == 'English-to-Hindi':
            try:
                translated_word = GoogleTranslator(source='en', target='hi').translate(input_text)
                output.insert('end', f" {translated_word}\n")
            except Exception as e:
                messagebox.showerror('Error', f"Translation failed. {e}")

    elif selected_option.get() == "Sentence":
        try:
            translated_sentence = GoogleTranslator(source='en', target='hi').translate(input_text)
            output.insert('end', f" {translated_sentence}\n")
        except Exception as e:
            messagebox.showerror('Error', f"Translation failed. {e}")

def clear_output():
    output.delete('1.0', END)

def quit_app():
    root.destroy()

# Grid Layout - Improved Alignment and Padding
frame_top = Frame(root, bg="#F8F8F8")
frame_top.pack(pady=10)

Label(frame_top, text="Enter Word or Sentence:", font=('Arial', 12, 'bold'), bg="#F8F8F8").grid(row=0, column=0, sticky=W, padx=5)
entry = Entry(frame_top, width=40, font=('Arial', 12), borderwidth=2, relief=RIDGE)
entry.grid(row=0, column=1, padx=5)

try:
    speaker_icon = ImageTk.PhotoImage(Image.open(r'Translator/volume-low-solid.png').resize((20, 20)))
    Button(frame_top, image=speaker_icon, command=speak_input_text, relief=FLAT, bg="#F8F8F8").grid(row=0, column=2, padx=5)
except Exception:
    messagebox.showwarning('Image Error', 'Speaker icon not found!')

# Dropdown menu and radio buttons
frame_options = Frame(root, bg="#F8F8F8")
frame_options.pack(pady=10)

a = tk.StringVar()
language_combo = ttk.Combobox(frame_options, width=20, textvariable=a, state='readonly', font=('Arial', 10))
language_combo['values'] = ('English-to-English', 'English-to-Hindi')
language_combo.grid(row=1, column=1, padx=10)
language_combo.current(0)

selected_option = StringVar(value="Word")
Radiobutton(frame_options, text="Word", variable=selected_option, value="Word", bg="#F8F8F8", font=('Arial', 10)).grid(row=0, column=0, padx=5)
Radiobutton(frame_options, text="Sentence", variable=selected_option, value="Sentence", bg="#F8F8F8", font=('Arial', 10)).grid(row=0, column=1, padx=5)

Button(frame_options, text="Translate", font=('Arial', 10, 'bold'), command=get_meaning_or_translation).grid(row=1, column=0, padx=5)
Button(frame_options, text="Clear", font=('Arial', 10, 'bold'), command=clear_output).grid(row=1, column=2, padx=5)
Button(frame_options, text="Quit", font=('Arial', 10, 'bold'), command=quit_app).grid(row=1, column=3, padx=5)

# Output text box and speaker button for output
frame_output = Frame(root, bg="#F8F8F8")
frame_output.pack(pady=10)

Label(frame_output, text="Meaning/Translation:", font=('Arial', 12, 'bold'), bg="#F8F8F8").grid(row=0, column=0, sticky=W, padx=5)
output = Text(frame_output, height=8, width=70, font=('Arial', 10), borderwidth=2, relief=RIDGE)
output.grid(row=1, column=0, padx=5)

try:
    Button(frame_output, image=speaker_icon, command=speak_output_text, relief=FLAT, bg="#F8F8F8").grid(row=1, column=1, padx=5)
except Exception:
    messagebox.showwarning('Image Error', 'Speaker icon not found!')

root.mainloop()
