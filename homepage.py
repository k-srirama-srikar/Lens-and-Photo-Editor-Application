import customtkinter as ctk
import tkinter as tk
from PIL import Image

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("Lens And Photo Editor Application")
# app.geometry("1920x1080")
# app.state("zoomed")
app.after(0, lambda: app.state("zoomed"))
app.geometry("{0}x{1}+0+0".format(app.winfo_screenwidth(), app.winfo_screenheight()))
app.configure(bg_color="black", fg_color="black")
app.iconbitmap("media/IIT_PKD_bl.ico")
canvas1 = ctk.CTkCanvas(master=app, height=app.winfo_screenheight(), width=app.winfo_screenwidth(), borderwidth=0,
                        bg="black", highlightthickness=0)
canvas1.pack(fill="both", expand=True)
bg_img = tk.PhotoImage(file="media/bginsti4.png")
canvas1.create_image(0, 0, image=bg_img, anchor="nw")




def open_editor():
    # app.quit()
    app.destroy()
        import editor
        editor.start_editor()
    # editorv1.app1.mainloop()



    # from claszoomtk import PhotoEdit1
    # import claszoomtk
    # claszoomtk.app1.mainloop()

    # app1 = ctk.CTk()
    #
    # PhotoEdit1(app=app1)
    #
    # app1.mainloop()


def open_lens():
    app.destroy()
        from lens import start_lens
        start_lens()





edit_logo = ctk.CTkImage(light_image=Image.open("media/editorlogo.png"), dark_image=Image.open("media/editorlogo.png"),
                         size=(150, 150))
lens_logo = ctk.CTkImage(light_image=Image.open("media/len_logo.png"), dark_image=Image.open("media/len_logo.png"),
                         size=(150, 150))

editor_btn = ctk.CTkButton(master=app, text='', width=148, height=148, corner_radius=16, bg_color='black',
                           fg_color='transparent',
                           image=edit_logo, command=open_editor, hover_color="#242424")
editor_btn.place(relx=0.85, rely=0.30, anchor="center")

lens_btn = ctk.CTkButton(master=app, text='', width=148, height=148, corner_radius=16, bg_color='black',
                         fg_color='transparent', image=lens_logo, command=open_lens,
                         hover_color="#242424")
lens_btn.place(relx=0.15, rely=0.30, anchor="center")

app.mainloop()
