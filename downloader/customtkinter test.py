import customtkinter as tk

linktogoogle = 0

def button_callback():
    print("button clicked")
    print(link.get())
    global linktogoogle
    linktogoogle = f"https://www.youtube.com/results?search_query={link.get()}"
    print(linktogoogle)

app = tk.CTk()
app.geometry("400x150")


link = tk.CTkEntry(app, placeholder_text="link")
link.pack()

button = tk.CTkButton(app, text="submit", command=button_callback)
button.pack()



app.mainloop()