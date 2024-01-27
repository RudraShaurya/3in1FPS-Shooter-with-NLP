import openai
from tkinter import *
from tkinter import ttk
from settings import SECRET_KEY, PROMPT


string = ''
l = []

# Create an instance of Tkinter frame
win = Tk()
win.title('Bandler\'s Legacy')
# Set the geometry of Tkinter frame
win.geometry("800x200")


def display_text():
    global entry, string
    string = entry.get()
    l.append(string)
    win.destroy()


# Create an Entry widget to accept User Input
entry = Entry(win, width=50, justify=CENTER)
entry.focus_set()
entry.pack(pady=50)

# Create a Button to validate Entry Widget
ttk.Button(win, text="Enter", width=20, command=display_text).pack()
win.mainloop()
print(l[0])

# openai davinci-text-002 pretrained NLP model, promtpt = query
openai.api_key = SECRET_KEY
s = l[0]
prompt = PROMPT + s
response = openai.Completion.create(
    engine='text-davinci-002',
    prompt=prompt,
    max_tokens=1000,
    n=1,
    temperature=0.3,
)

response_text = response.choices[0].text
genre = 'horror'

# checking response text for the genre
if 'Horror' in response_text:
    genre = 'horror'
elif 'Adventure' in response_text:
    genre = 'adventure'
elif 'Fantasy' in response_text:
    genre = 'fantasy'
