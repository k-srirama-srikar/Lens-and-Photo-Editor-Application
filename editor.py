import customtkinter as ctk
from tkinter import filedialog, colorchooser, ROUND
import numpy as np
import cv2
from PIL import Image, ImageTk, ImageEnhance

ctk.set_appearance_mode("dark")


class PhotoEdit1:
    def __init__(self, app):
        self.undo_saves = []
        self.redo_saves = []
        self.adjust_values = {"brightness": 1,
                              "contrast": 1,
                              "sharpness": 1,
                              "saturation": 0,
                              "colour": 1}
        self.adjust_undo_values = {"brightness": [1],
                                   "contrast": [1],
                                   "sharpness": [1],
                                   "saturation": [0],
                                   "colour": [1]}
        self.adjust_redo_values = {"brightness": [],
                                   "contrast": [],
                                   "sharpness": [],
                                   "saturation": [],
                                   "colour": []}
        self.blur_values = {"average": 0,
                            "gaussian": 0,
                            "median": 0}
        self.blur_undo_value = {"average": [0],
                                "gaussian": [0],
                                "median": [0]}
        self.blur_redo_value = {"average": [],
                                "gaussian": [],
                                "median": []}
        self.color_code = None
        self.new_image = None
        self.ratio = None
        self.text_on_img = None
        self.text_inp = None
        self.filtered_img = None
        self.edited_img = None
        self.original_img = None
        self.filename = None
        self.side_frame = None
        self.bottom_frame = None
        self.canvas = None
        self.text_fonts = ["Comic Sans", "Comic Sans Small", "Comic Sans Bold", "Monospace", "Monospace Bold",
                           "Monospace Small", "Cursive #1", "Cursive #2"]
        self.app = app
        self.initialisation()

    def initialisation(self):

        self.app.title("Photo Editor")
        self.app.geometry("{0}x{1}+0+0".format(self.app.winfo_screenwidth(), self.app.winfo_screenheight()))
        # self.app.state('zoomed')
        # app.state("zoomed")
        self.app.after(0, lambda: self.app.state("zoomed"))
        self.app.iconbitmap("media/editorico.ico")

        self.home_logo = ctk.CTkImage(light_image=Image.open("media/home button.png"),
                                      dark_image=Image.open("media/home button.png"),
                                      size=(20, 20))
        self.editor_btn = ctk.CTkButton(master=self.app, text='', width=20, corner_radius=0, bg_color='black',
                                        fg_color='transparent',
                                        image=self.home_logo, command=self.home_page, hover_color="#242424")
        self.editor_btn.place(relx=0.0, rely=0.0, anchor="nw")

        self.upload_an_image = ctk.CTkButton(
            master=self.app, text="Upload an Image", command=self.upload_button,
            hover_color="#242424", corner_radius=0, fg_color="transparent"
        )
        self.upload_an_image.place(relx=0.018, rely=0, anchor="nw")

        self.save_as = ctk.CTkButton(
            master=self.app, text="Save As", command=self.save_action,
            hover_color="#242424", corner_radius=0, fg_color="transparent", state="disabled"
        )
        self.save_as.place(relx=0.108, rely=0, anchor="nw")

        self.default_img = cv2.imread("media/canv12.png")

        self.disp_default_img = ImageTk.PhotoImage(Image.fromarray(self.default_img))

        self.canvas = ctk.CTkCanvas(
            master=self.app, width=1200, height=800, bg="black",
            highlightthickness=0)

        self.canvas.create_image(600, 400, image=self.disp_default_img)

        self.canvas.place(relx=0.47, rely=0.5, anchor="center")

        self.apply_button = ctk.CTkButton(
            master=self.app, text="Apply", command=self.apply_action,
            hover_color="#242424", corner_radius=0, fg_color="transparent", state="disabled"
        )
        self.apply_button.place(relx=0.198, rely=0, anchor="nw")

        self.cancel_button = ctk.CTkButton(
            master=self.app, text="Cancel", command=self.cancel_action,
            hover_color="#242424", corner_radius=0, fg_color="transparent", state="disabled"
        )
        self.cancel_button.place(relx=0.288, rely=0, anchor="nw")

        self.undo_all_changes = ctk.CTkButton(
            master=self.app, text="Undo all changes", command=self.revert_action,
            hover_color="#242424", corner_radius=0, fg_color="transparent", state="disabled"
        )
        self.undo_all_changes.place(relx=0.378, rely=0, anchor="nw")

        self.undo_button = ctk.CTkButton(
            master=self.app, text="Undo", command=self.undo_action,
            hover_color="#242424", corner_radius=0, fg_color="transparent", state="disabled"
        )
        self.undo_button.place(relx=0.468, rely=0, anchor="nw")

        self.redo_button = ctk.CTkButton(
            master=self.app, text="Redo", command=self.redo_action,
            hover_color="#242424", corner_radius=0, fg_color="transparent", state="disabled"
        )
        self.redo_button.place(relx=0.558, rely=0, anchor="nw")
        self.bottom_frame = ctk.CTkFrame(master=self.app, width=300, height=50, fg_color="transparent",
                                         bg_color="transparent")

        self.bottom_frame.place(relx=0.47, rely=0.95, anchor="center")





    def home_page(self):
        self.app.destroy()
        import homepage

        try:
            homepage.app.mainloop()
        except:
            homepage.app = ctk.CTk()
            homepage.app.mainloop()

    def upload_button(self):
        self.canvas.delete("all")
        self.filename = filedialog.askopenfilename()
        self.original_img = cv2.imread(self.filename)

        self.edited_img = cv2.imread(self.filename)
        self.filtered_img = cv2.imread(self.filename)
        self.display_image(cv2.imread(self.filename))

        self.refresh_side_frame()
        ctk.CTkLabel(master=self.bottom_frame,
                     text="Don't forget to click on apply whenever you want to save changes to the image",
                     text_color="#63666a"
                     ).grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        self.save_as.configure(state="normal")
        self.apply_button.configure(state="normal")
        self.cancel_button.configure(state="normal")
        self.undo_all_changes.configure(state="normal")
        self.undo_button.configure(state="normal")
        self.redo_button.configure(state="normal")
        self.left_frame()

    def left_frame(self):
        self.left_side_frame = ctk.CTkFrame(master=self.app, width=250, height=650,
                                            bg_color="transparent", fg_color="transparent")
        self.left_side_frame.place(relx=0.01, rely=0.5, anchor="w")

        ctk.CTkButton(
            master=self.left_side_frame, text="Crop", command=self.crop_action,
            hover_color="#242424", corner_radius=32, border_color="#ffad00", border_width=2, fg_color="black"
        ).grid(row=2, column=0, padx=5, pady=5)

        ctk.CTkButton(
            master=self.left_side_frame, text="Add Text", command=self.text_button,
            hover_color="#242424", corner_radius=32, border_color="#ffad00", border_width=2, fg_color="black"
        ).grid(row=3, column=0, padx=5, pady=5)

        ctk.CTkButton(
            master=self.left_side_frame, text="Draw", command=self.draw_button,
            hover_color="#242424", corner_radius=32, border_color="#ffad00", border_width=2, fg_color="black"
        ).grid(row=4, column=0, padx=5, pady=5)

        ctk.CTkButton(
            master=self.left_side_frame, text="Apply Filters", command=self.filter_action,
            hover_color="#242424", corner_radius=32, border_color="#ffad00", border_width=2, fg_color="black"
        ).grid(row=5, column=0, padx=5, pady=5)

        ctk.CTkButton(
            master=self.left_side_frame, text="Blur", command=self.blur_action,
            hover_color="#242424", corner_radius=32, border_color="#ffad00", border_width=2, fg_color="black"
        ).grid(row=6, column=0, padx=5, pady=5)

        ctk.CTkButton(
            master=self.left_side_frame, text="Adjust", command=self.adjust_action,
            hover_color="#242424", corner_radius=32, border_color="#ffad00", border_width=2, fg_color="black"
        ).grid(row=7, column=0, padx=5, pady=5)

        ctk.CTkButton(
            master=self.left_side_frame, text="Rotate", command=self.rotate_action,
            hover_color="#242424", corner_radius=32, border_color="#ffad00", border_width=2, fg_color="black"
        ).grid(row=8, column=0, padx=5, pady=5)

        ctk.CTkButton(
            master=self.left_side_frame, text="Flip", command=self.flip_action,
            hover_color="#242424", corner_radius=32, border_color="#ffad00", border_width=2, fg_color="black"
        ).grid(row=9, column=0, padx=5, pady=5)

        ctk.CTkButton(
            master=self.left_side_frame, text="Preview", command=self.preview_action,
            hover_color="#242424", corner_radius=32, border_color="#ffad00", border_width=2, fg_color="black"
        ).grid(row=10, column=0, padx=5, pady=5)

    def text_button(self):
        self.text_inp = "Hello World --Python"
        self.refresh_side_frame()
        ctk.CTkLabel(
            master=self.side_frame, text="Enter text:"
        ).grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        self.text_on_img = ctk.CTkEntry(self.side_frame)
        self.text_on_img.grid(row=1, column=2, padx=5, sticky="nw")
        ctk.CTkButton(
            master=self.side_frame, text="Pick a Font Color",
            command=self.choose_color, hover_color="#242424", border_color="#ffad00", border_width=2, fg_color="black"
        ).grid(row=2, column=2, padx=5, pady=5, sticky="nw")
        self.text_action()
        ctk.CTkLabel(
            master=self.side_frame, text="Choose a Font"
        ).grid(row=3, column=2, padx=5, pady=1, sticky="nw")
        self.text_opt = ctk.CTkOptionMenu(master=self.side_frame,
                                          values=self.text_fonts,
                                          command=self.choose_font,
                                          button_color="#ffad00",
                                          fg_color="#242424",
                                          button_hover_color="#ff7400",
                                          dropdown_fg_color="black",
                                          dropdown_hover_color="#242424"
                                          )
        self.text_opt.grid(row=4, column=2, padx=5, pady=5, sticky="nw")
        ctk.CTkLabel(
            master=self.bottom_frame, text="Choose a color and font and "
                                           "select a point and drag to get the text on image",
            text_color="#63666a", anchor="w"
        ).grid(row=5, column=2, padx=5, pady=10, sticky="nw")
        # print(self.text_opt)

    def crop_action(self):
        self.refresh_side_frame()
        self.rectangle = 0
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_end_y = 0
        self.crop_end_x = 0
        ctk.CTkLabel(master=self.bottom_frame,
                     text="Select a point and drag to get the cropped image",
                     text_color="#63666a"
                     ).grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        self.canvas.bind("<ButtonPress>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.crop)
        self.canvas.bind("<ButtonRelease>", self.end_crop)

    def start_crop(self, event):
        self.crop_start_x = event.x
        self.crop_start_y = event.y

    def crop(self, event):
        if self.rectangle:
            self.canvas.delete(self.rectangle)
        self.crop_end_x = event.x
        self.crop_end_y = event.y
        self.rectangle = self.canvas.create_rectangle(self.crop_start_x,
                                                      self.crop_start_y,
                                                      self.crop_end_x,
                                                      self.crop_end_y,
                                                      width=1)

    def end_crop(self, event):
        if self.crop_start_x <= self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif self.crop_start_x > self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif self.crop_start_x <= self.crop_end_x and self.crop_start_y > self.crop_end_y:
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)
        else:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)
        x = slice(start_x, end_x, 1)
        y = slice(start_y, end_y, 1)
        self.filtered_img = self.edited_img[y, x]
        self.display_image(self.filtered_img)

    def text_action(self):
        self.rectangle = 0
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_end_x = 0
        self.crop_end_y = 0
        self.canvas.bind("<ButtonPress>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.crop)
        self.canvas.bind("<ButtonRelease>", self.end_text_crop)

    def choose_font(self, choice):
        # print(choice)
        self.text_font = self.text_fonts[0]
        self.text_font = choice
        # print(self.text_font)

    def end_text_crop(self, event):
        if self.crop_start_x <= self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif self.crop_start_x > self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif self.crop_start_x <= self.crop_end_x and self.crop_start_y > self.crop_end_y:
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)
        else:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)

        if self.text_on_img.get():
            self.text_inp = self.text_on_img.get()
        start_font = start_x, start_y
        # print(self.color_code)
        if self.color_code != None and len(self.color_code) == 2:
            r, g, b = tuple(map(int, self.color_code[0]))
        else:
            r, g, b = (255, 255, 255)
        self.text_font_no = 0

        try:
            # self.text_font != None
            self.text_font_no = self.text_fonts.index(self.text_font)
        except AttributeError:
            self.text_font_no = 0
        self.filtered_img = cv2.putText(self.filtered_img.copy(), self.text_inp, start_font, self.text_font_no, 2,
                                        (b, g, r), 5)

        self.display_image(self.filtered_img)

    def draw_button(self):
        self.color_code = (255, 0, 0)
        self.refresh_side_frame()
        self.canvas.bind("<ButtonPress>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.draw_color_button = ctk.CTkButton(master=self.side_frame, text="Pick a Color", command=self.choose_color,
                                               hover_color="#242424", border_color="#ffad00",
                                               border_width=2, fg_color="black")
        self.draw_color_button.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        ctk.CTkLabel(
            master=self.bottom_frame, text="Pick a colour and click and move along the image to draw",
            text_color="#63666a", anchor="w"
        ).grid(row=5, column=2, padx=5, pady=10, sticky="nw")

    def choose_color(self):
        self.color_code = ((255, 255, 255), "#ffffff")
        self.color_code = colorchooser.askcolor(title="Pick a Color")

    def start_draw(self, event):
        self.x = event.x
        self.y = event.y
        self.draw_ids = []

    def draw(self, event):
        # print(self.draw_ids)
        self.draw_ids.append(self.canvas.create_line(self.x, self.y, event.x, event.y, width=2,
                                                     fill=self.color_code[-1], capstyle=ROUND, smooth=True))
        # print(self.color_code)
        r, g, b = tuple(map(int, self.color_code[0]))
        cv2.line(self.filtered_img, pt1=(int(self.x * self.ratio), int(self.y * self.ratio)),
                 pt2=(int(event.x * self.ratio), int(event.y * self.ratio)), color=(b, g, r),
                 lineType=8, thickness=int(self.ratio * 2))
        self.x = event.x
        self.y = event.y

    def refresh_side_frame(self):
        self.cancel_action()
        # self.side_frame.delete("all")
        try:
            self.side_frame.destroy()
            self.bottom_frame.destroy()
        except:
            pass
        try:
            self.preview_window.withdraw()
        except:
            pass
        self.canvas.unbind("<ButtonPress>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease>")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<MouseWheel>")
        self.display_image(self.edited_img)
        self.side_frame = ctk.CTkFrame(master=self.app, width=250, height=600, fg_color="transparent")
        self.side_frame.place(relx=0.82, rely=0.5, anchor="w")
        self.bottom_frame = ctk.CTkFrame(master=self.app, width=300, height=50, fg_color="transparent",
                                         bg_color="transparent")
        self.bottom_frame.place(relx=0.47, rely=0.95, anchor="center")
        # self.side_frame.configure(padding=(50, 15))

    def filter_action(self):
        self.refresh_side_frame()
        ctk.CTkButton(
            master=self.side_frame, text="Negative", command=self.negative_action,
            hover_color="#242424", border_color="#ffad00",
            border_width=2, fg_color="black"
        ).grid(row=0, column=2, padx=5, pady=5, sticky="ne")

        ctk.CTkButton(
            master=self.side_frame, text="Black & White", command=self.bw_action,
            hover_color="#242424", border_color="#ffad00",
            border_width=2, fg_color="black"
        ).grid(row=1, column=2, padx=5, pady=5, sticky="ne")

        ctk.CTkButton(
            master=self.side_frame, text="Stylisation", command=self.stylisation_action,
            hover_color="#242424", border_color="#ffad00",
            border_width=2, fg_color="black"
        ).grid(row=2, column=2, padx=5, pady=5, sticky="ne")

        ctk.CTkButton(
            master=self.side_frame, text="Sketch Effect", command=self.sketch_action,
            hover_color="#242424", border_color="#ffad00",
            border_width=2, fg_color="black"
        ).grid(row=3, column=2, padx=5, pady=5, sticky="ne")

        ctk.CTkButton(
            master=self.side_frame, text="Emboss", command=self.emb_action,
            hover_color="#242424", border_color="#ffad00",
            border_width=2, fg_color="black"
        ).grid(row=4, column=2, padx=5, pady=5, sticky="ne")

        ctk.CTkButton(
            master=self.side_frame, text="Sepia", command=self.sepia_action,
            hover_color="#242424", border_color="#ffad00",
            border_width=2, fg_color="black"
        ).grid(row=5, column=2, padx=5, pady=5, sticky="ne")

        ctk.CTkButton(
            master=self.side_frame, text="Binary Thresholding", command=self.binary_threshold_action,
            hover_color="#242424", border_color="#ffad00",
            border_width=2, fg_color="black"
        ).grid(row=6, column=2, padx=5, pady=5, sticky="ne")

        ctk.CTkButton(
            master=self.side_frame, text="Erosion", command=self.erosion_action,
            hover_color="#242424", border_color="#ffad00",
            border_width=2, fg_color="black"
        ).grid(row=7, column=2, padx=5, pady=5, sticky="ne")

        ctk.CTkButton(
            master=self.side_frame, text="Dilation", command=self.dilation_action,
            hover_color="#242424", border_color="#ffad00",
            border_width=2, fg_color="black"
        ).grid(row=8, column=2, padx=5, pady=5, sticky="ne")

        ctk.CTkLabel(
            master=self.bottom_frame, text="Select any of the filters and press apply if you want them",
            text_color="#63666a", anchor="w"
        ).grid(row=5, column=2, padx=5, pady=10, sticky="nw")

    def blur_action(self):
        self.refresh_side_frame()
        ctk.CTkLabel(
            master=self.side_frame, text="Averaging Blur",
        ).grid(row=0, column=2, padx=5, sticky="nw")

        self.average_slider = ctk.CTkSlider(
            master=self.side_frame, from_=0, to=256, orientation="horizontal",
            command=self.averaging_action, button_color="#ffad00", button_hover_color="#ff7400"
        )
        self.average_slider.set(self.blur_values["average"])
        self.average_slider.grid(row=1, column=2, padx=5, sticky="nw")

        ctk.CTkLabel(
            master=self.side_frame, text="Gaussian Blur"
        ).grid(row=2, column=2, padx=5, sticky="nw")

        self.gaussian_slider = ctk.CTkSlider(
            master=self.side_frame, from_=0, to=256, orientation="horizontal",
            command=self.gaussian_action, button_color="#ffad00", button_hover_color="#ff7400"
        )
        self.gaussian_slider.set(self.blur_values["gaussian"])
        self.gaussian_slider.grid(row=3, column=2, padx=5, sticky="nw")

        ctk.CTkLabel(
            master=self.side_frame, text="Median Blur"
        ).grid(row=4, column=2, padx=5, sticky="nw")

        self.median_slider = ctk.CTkSlider(
            master=self.side_frame, from_=0, to=256, orientation="horizontal",
            command=self.median_action, button_color="#ffad00", button_hover_color="#ff7400"
        )
        self.median_slider.set(self.blur_values["median"])
        self.median_slider.grid(row=5, column=2, padx=5, sticky="nw")

        ctk.CTkLabel(master=self.bottom_frame,
                     text="Move the slider to modify the image and click on apply",
                     text_color="#63666a"
                     ).grid(row=0, column=2, padx=5, pady=5, sticky="nw")


    def rotate_action(self):
        self.refresh_side_frame()
        ctk.CTkButton(
            master=self.side_frame, text="Rotate Left", command=self.rotate_left_action,
            hover_color="#242424", border_color="#ffad00",
            border_width=2, fg_color="black"
        ).grid(
            row=0, column=2, padx=5, pady=5, sticky='sw')

        ctk.CTkButton(
            self.side_frame, text="Rotate Right", command=self.rotate_right_action,
            hover_color="#242424", border_color="#ffad00",
            border_width=2, fg_color="black"
        ).grid(
            row=1, column=2, padx=5, pady=5, sticky='sw')

        ctk.CTkLabel(master=self.bottom_frame,
                     text="Press the button to rotate the direction in which you want",
                     text_color="#63666a"
                     ).grid(row=0, column=2, padx=5, pady=5, sticky="nw")

    def flip_action(self):
        self.refresh_side_frame()
        ctk.CTkButton(
            master=self.side_frame, text="Vertical Flip", command=self.vertical_action,
            hover_color="#242424", border_color="#ffad00",
            border_width=2, fg_color="black"
        ).grid(
            row=0, column=2, padx=5, pady=5, sticky='se')

        ctk.CTkButton(
            master=self.side_frame, text="Horizontal Flip", command=self.horizontal_action,
            hover_color="#242424", border_color="#ffad00",
            border_width=2, fg_color="black"
        ).grid(
            row=1, column=2, padx=5, pady=5, sticky='se')

        ctk.CTkLabel(master=self.bottom_frame,
                     text="press the button to flip the image in whichever direction you want",
                     text_color="#63666a"
                     ).grid(row=0, column=2, padx=5, pady=5, sticky="nw")

    def adjust_action(self):
        self.refresh_side_frame()
        try:
            self.apply_action()
        except:
            pass

        ctk.CTkLabel(master=self.bottom_frame,
                     text="Move the slider to modify the image and click on apply",
                     text_color="#63666a"
                     ).grid(row=0, column=2, padx=5, pady=5, sticky="nw")

        # Brightness

        ctk.CTkLabel(
            master=self.side_frame, text="Brightness"
        ).grid(row=0, column=2, padx=5, pady=5, sticky="nw")


        self.brightness_slider = ctk.CTkSlider(
            master=self.side_frame, from_=0, to=2, number_of_steps=20, command=self.brightness_action,
            button_color="#ffad00", button_hover_color="#ff7400"
        )
        self.brightness_slider.grid(row=1, column=2, padx=5, sticky='nw')
        self.brightness_slider.set(self.adjust_values["brightness"])

        # Saturation

        ctk.CTkLabel(
            master=self.side_frame, text="Saturation"
        ).grid(row=3, column=2, padx=5, pady=5, sticky="nw")

        self.saturation_slider = ctk.CTkSlider(
            master=self.side_frame, from_=-200, to=200, command=self.saturation_action,
            button_color="#ffad00", button_hover_color="#ff7400"

        )
        self.saturation_slider.grid(row=4, column=2, padx=5, sticky='nw')
        self.saturation_slider.set(self.adjust_values["saturation"])

        # Contrast

        ctk.CTkLabel(
            master=self.side_frame, text="Contrast"
        ).grid(row=6, column=2, padx=5, pady=5, sticky="nw")

        self.contrast_slider = ctk.CTkSlider(
            master=self.side_frame, from_=0, to=10, number_of_steps=20, command=self.contrast_action,
            button_color="#ffad00", button_hover_color="#ff7400"

        )
        self.contrast_slider.grid(row=7, column=2, padx=5, sticky='nw')
        self.contrast_slider.set(self.adjust_values["contrast"])

        # Sharpness

        ctk.CTkLabel(
            master=self.side_frame, text="Sharpness"
        ).grid(row=9, column=2, padx=5, pady=5, sticky="nw")

        self.sharpness_slider = ctk.CTkSlider(
            master=self.side_frame, from_=0, to=20, number_of_steps=20, command=self.sharpness_action,
            button_color="#ffad00", button_hover_color="#ff7400"
        )
        self.sharpness_slider.grid(row=10, column=2, padx=5, sticky='nw')
        self.sharpness_slider.set(self.adjust_values["sharpness"])

        # Colour

        ctk.CTkLabel(
            master=self.side_frame, text="Colour"
        ).grid(row=12, column=2, padx=5, pady=5, sticky="nw")

        self.color_slider = ctk.CTkSlider(
            master=self.side_frame, from_=-10, to=10, number_of_steps=20, command=self.colour_action,
            button_color="#ffad00", button_hover_color="#ff7400"
        )
        self.color_slider.grid(row=13, column=2, padx=5, sticky='nw')
        self.color_slider.set(self.adjust_values["colour"])

    def save_action(self):
        original_file_type = self.filename.split(".")[-1]
        filename = filedialog.asksaveasfilename()
        filename = filename + "." + original_file_type

        saved_image = self.edited_img
        cv2.imwrite(filename, saved_image)
        self.filename = filename

    def negative_action(self):
        self.filtered_img = cv2.bitwise_not(self.edited_img)
        self.display_image(self.filtered_img)

    def bw_action(self):
        self.filtered_img = cv2.cvtColor(
            self.edited_img, cv2.COLOR_BGR2GRAY)
        self.filtered_img = cv2.cvtColor(
            self.filtered_img, cv2.COLOR_GRAY2BGR)
        self.display_image(self.filtered_img)

    def stylisation_action(self):
        self.filtered_img = cv2.stylization(
            self.edited_img, sigma_s=150, sigma_r=0.25)
        self.display_image(self.filtered_img)

    def sketch_action(self):
        ret, self.filtered_img = cv2.pencilSketch(
            self.edited_img, sigma_s=60, sigma_r=0.5, shade_factor=0.02)
        self.display_image(self.filtered_img)

    def emb_action(self):
        kernel = np.array([[0, -1, -1],
                           [1, 0, -1],
                           [1, 1, 0]])
        self.filtered_img = cv2.filter2D(self.original_img, -1, kernel)
        self.display_image(self.filtered_img)

    def sepia_action(self):
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])

        self.filtered_img = cv2.filter2D(self.original_img, -1, kernel)
        self.display_image(self.filtered_img)

    def binary_threshold_action(self):
        ret, self.filtered_img = cv2.threshold(
            self.edited_img, 127, 255, cv2.THRESH_BINARY)
        self.display_image(self.filtered_img)

    def erosion_action(self):
        kernel = np.ones((5, 5), np.uint8)
        self.filtered_img = cv2.erode(
            self.edited_img, kernel, iterations=1)
        self.display_image(self.filtered_img)

    def dilation_action(self):
        kernel = np.ones((5, 5), np.uint8)
        self.filtered_img = cv2.dilate(
            self.edited_img, kernel, iterations=1)
        self.display_image(self.filtered_img)

    def averaging_action(self, value):
        if self.check_blur_change("averaging"):
            self.blur_cancel()
            self.average_slider.set(value)
        value = int(value)
        if value % 2 == 0:
            value += 1
        self.filtered_img = cv2.blur(
            self.edited_img.copy(), (value, value))
        self.display_image(self.filtered_img)

    def gaussian_action(self, value):
        if self.check_blur_change("gaussian"):
            self.blur_cancel()
            self.gaussian_slider.set(value)
        value = int(value)
        if value % 2 == 0:
            value += 1
        self.filtered_img = cv2.GaussianBlur(
            self.edited_img.copy(), (value, value), 0
        )
        self.display_image(self.filtered_img)

    def median_action(self, value):
        if self.check_blur_change("median"):
            self.blur_cancel()
            self.median_slider.set(value)
        value = int(value)
        if value % 2 == 0:
            value += 1
        self.filtered_img = cv2.medianBlur(
            self.edited_img.copy(), value
        )
        self.display_image(self.filtered_img)

    def get_values(self):
        self.got_values = {"brightness": self.brightness_slider.get(),
                           "contrast": self.contrast_slider.get(),
                           "sharpness": self.sharpness_slider.get(),
                           "saturation": self.saturation_slider.get(),
                           "colour": self.color_slider.get()}

    def check_adjust_change(self, str):
        self.get_values()
        for key in self.adjust_values:
            if not key == str:
                if self.adjust_values[key] == self.got_values[key]:
                    continue
                else:
                    return True
        return False

    def check_blur_change(self, str):
        self.get_blur_values()
        for key in self.blur_values:
            if not key == str:
                if self.blur_values[key] == self.got_blur_values[key]:
                    continue
                else:
                    return True
        return False

    def get_blur_values(self):
        self.got_blur_values = {"average": self.average_slider.get(),
                                "gaussian": self.gaussian_slider.get(),
                                "median": self.median_slider.get()}

    def adjust_cancel(self):
        try:
            self.brightness_slider.set(self.adjust_values["brightness"])
            self.saturation_slider.set(self.adjust_values["saturation"])
            self.color_slider.set(self.adjust_values["colour"])
            self.sharpness_slider.set(self.adjust_values["sharpness"])
            self.contrast_slider.set(self.adjust_values["contrast"])
        except:
            pass

    def blur_cancel(self):
        self.average_slider.set(self.blur_values["average"])
        self.gaussian_slider.set(self.blur_values["gaussian"])
        self.median_slider.set(self.blur_values["median"])

    def blur_save_value(self):
        self.get_blur_values()
        # print(self.got_blur_values)
        for key in self.blur_values:
            if not self.blur_values[key] == self.got_blur_values[key]:
                self.blur_undo_value[key].insert(0, self.blur_values[key])
                self.blur_values[key] = self.got_blur_values[key]
                if len(self.blur_undo_value[key]) > 5:
                    self.blur_undo_value[key].pop(5)

    def save_value(self):
        self.get_values()
        for key in self.adjust_values:
            if not self.adjust_values[key] == self.got_values[key]:
                self.adjust_undo_values[key].insert(0, self.adjust_values[key])
                self.adjust_values[key] = self.got_values[key]
                if len(self.adjust_undo_values[key]) > 5:
                    self.adjust_undo_values[key].pop(5)

    def brightness_action(self, value):
        # self.filtered_img = np.array(
        #     ImageEnhance.Brightness(Image.fromarray(cv2.cvtColor(self.bs_img.copy(), cv2.COLOR_BGR2RGB))).enhance(
        #         self.brightness_slider.get()))
        # self.filtered_img = cv2.cvtColor(self.filtered_img, cv2.COLOR_RGB2BGR)
        # self.display_image(self.filtered_img)
        if self.check_adjust_change("brightness"):
            # self.adjust_values["brightness"] = value
            self.adjust_cancel()
            self.brightness_slider.set(value)
        self.filtered_img = cv2.convertScaleAbs(
            self.edited_img.copy(), alpha=self.brightness_slider.get())
        self.display_image(self.filtered_img)

    def saturation_action(self, value):
        if self.check_adjust_change("saturation"):
            self.adjust_cancel()
            self.saturation_slider.set(value)
        self.filtered_img = cv2.convertScaleAbs(
            self.edited_img.copy(), alpha=1, beta=self.saturation_slider.get())
        self.display_image(self.filtered_img)

    def contrast_action(self, value):
        if self.check_adjust_change("contrast"):
            self.adjust_cancel()
            self.contrast_slider.set(value)
        self.filtered_img = np.array(
            ImageEnhance.Contrast(Image.fromarray(cv2.cvtColor(self.edited_img.copy(), cv2.COLOR_BGR2RGB))).enhance(
                self.contrast_slider.get()))
        self.filtered_img = cv2.cvtColor(self.filtered_img.copy(), cv2.COLOR_RGB2BGR)
        self.display_image(self.filtered_img)

    def colour_action(self, value):
        if self.check_adjust_change("colour"):
            # self.adjust_values["colour"] = value
            self.adjust_cancel()
            self.color_slider.set(value)
        self.filtered_img = np.array(
            ImageEnhance.Color(Image.fromarray(cv2.cvtColor(self.edited_img.copy(), cv2.COLOR_BGR2RGB))).enhance(
                self.color_slider.get()))
        self.filtered_img = cv2.cvtColor(self.filtered_img.copy(), cv2.COLOR_RGB2BGR)
        self.display_image(self.filtered_img)

    def sharpness_action(self, value):
        if self.check_adjust_change("sharpness"):
            # self.adjust_values["sharpness"] = value
            self.adjust_cancel()
            self.sharpness_slider.set(value)
        self.filtered_img = np.array(
            ImageEnhance.Sharpness(Image.fromarray(cv2.cvtColor(self.edited_img.copy(), cv2.COLOR_BGR2RGB))).enhance(
                self.sharpness_slider.get()))
        self.filtered_img = cv2.cvtColor(self.filtered_img.copy(), cv2.COLOR_RGB2BGR)
        self.display_image(self.filtered_img)

    def rotate_left_action(self):
        self.filtered_img = cv2.rotate(
            self.filtered_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.display_image(self.filtered_img)

    def rotate_right_action(self):
        self.filtered_img = cv2.rotate(
            self.filtered_img, cv2.ROTATE_90_CLOCKWISE)
        self.display_image(self.filtered_img)

    def vertical_action(self):
        self.filtered_img = cv2.flip(self.filtered_img, 0)
        self.display_image(self.filtered_img)

    def horizontal_action(self):
        self.filtered_img = cv2.flip(self.filtered_img, 1)
        self.display_image(self.filtered_img)

    def apply_action(self):
        if not np.array_equal(self.edited_img.copy(), self.filtered_img.copy()):
            self.undo_save(self.edited_img.copy())
            try:
                self.save_value()
            except:
                pass
            try:
                self.blur_save_value()
            except:
                pass
            self.edited_img = self.filtered_img.copy()
            self.display_image(self.edited_img)

    def undo_save(self, img):
        self.undo_saves.insert(0, img)

        if len(self.undo_saves) > 5:
            self.undo_saves.pop(5)

    def undo_blur_action(self):
        for key in self.blur_values:
            if len(self.blur_undo_value[key]) > 0:
                self.blur_redo_value[key].insert(0, self.blur_values[key])
                self.blur_values[key] = self.blur_undo_value[key].pop(0)
        self.blur_cancel()

    def redo_blur_action(self):
        for key in self.blur_values:
            if len(self.blur_redo_value[key]) > 0:
                self.blur_undo_value[key].insert(0, self.blur_values[key])
                self.blur_values[key] = self.blur_redo_value[key].pop(0)
        self.blur_cancel()

    def undo_adjust_action(self):
        for key in self.adjust_values:
            if len(self.adjust_undo_values[key]) > 0:
                self.adjust_redo_values[key].insert(0, self.adjust_values[key])
                self.adjust_values[key] = self.adjust_undo_values[key].pop(0)
        self.adjust_cancel()

    def redo_adjust_action(self):
        for key in self.adjust_values:
            if len(self.adjust_redo_values[key]) > 0:
                self.adjust_undo_values[key].insert(0, self.adjust_values[key])
                self.adjust_values[key] = self.adjust_redo_values[key].pop(0)
        self.adjust_cancel()

    def redo_save(self, img):
        self.redo_saves.insert(0, img)

    def undo_action(self):
        if len(self.undo_saves) > 0:
            self.redo_save(self.edited_img.copy())
            self.edited_img = self.undo_saves[0].copy()
            self.filtered_img = self.edited_img.copy()
            self.undo_saves.pop(0)
            try:
                self.undo_blur_action()
            except:
                pass
            try:
                self.undo_adjust_action()
            except:
                pass
            self.display_image(self.edited_img)

    def redo_action(self):
        if len(self.redo_saves) > 0:
            self.undo_save(self.edited_img)
            self.edited_img = self.redo_saves[0].copy()
            self.filtered_img = self.edited_img.copy()
            self.redo_saves.pop(0)
            try:
                self.redo_adjust_action()
            except:
                pass
            try:
                self.redo_blur_action()
            except:
                pass
            self.display_image(self.edited_img)

    def cancel_action(self):
        self.filtered_img = self.edited_img.copy()
        try:
            self.adjust_cancel()
        except:
            pass
        try:
            self.blur_cancel()
        except:
            pass
        # self.refresh_side_frame()
        self.display_image(self.edited_img)

    def revert_action(self):
        self.undo_saves = []
        self.adjust_values["brightness"] = 1
        self.adjust_values["contrast"] = 1
        self.adjust_values["sharpness"] = 1
        self.adjust_values["colour"] = 1
        self.adjust_values["saturation"] = 0
        try:
            self.adjust_cancel()
            self.save_value()
        except:
            pass
        self.blur_values["average"] = 0
        self.blur_values["gaussian"] = 0
        self.blur_values["median"] = 0
        try:
            self.blur_cancel()
            self.blur_save_value()
        except:
            pass
        self.redo_save(self.filtered_img.copy())
        self.filtered_img = self.original_img.copy()
        self.edited_img = self.original_img.copy()
        self.display_image(self.edited_img)

    def preview_action(self):
        self.preview_window = ctk.CTkToplevel(self.app)
        self.preview_window.geometry('400x400+1400+500')
        self.preview_window.title("Preview Window")
        self.preview_window.withdraw()
        self.preview_window.lift()
        # self.preview_window.protocol('WM_DELETE_WINDOW',self.preview_window.destroy())
        self.refresh_side_frame()
        ctk.CTkLabel(master=self.bottom_frame,
                     text="Select a point or hold the mouse 1 button and move through the image to see its preview"
                     "\nScroll up or down to increase or decrease the zoom level",
                     text_color="#63666a"
                     ).grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        self.copimg = self.edited_img.copy()
        t0img = cv2.cvtColor(self.copimg, cv2.COLOR_BGR2RGB)
        self.t1img = Image.fromarray(t0img)
        copw, coph = self.t1img.size
        if copw > 1200 or coph > 800:
            asp_rat = min(1200 / copw, 800 / coph)
            copw = copw * asp_rat
            coph = coph * asp_rat
        self.t1img = self.t1img.resize((int(copw), int(coph)))
        self.prv_lbl = ctk.CTkLabel(self.preview_window, text='')
        self.prv_lbl.pack()
        self.zoom_label = ctk.CTkLabel(self.side_frame, text="Zoom Level")
        self.zoom_label.pack()
        self.canvas.bind("<Button-1>", self.zooming)
        self.zoom_slider = ctk.CTkSlider(self.side_frame, from_=1, to=5,
                                         button_color="#ffad00", button_hover_color="#ff7400")
        self.zoom_slider.pack()
        self.canvas.bind("<B1-Motion>", self.zooming)
        self.canvas.bind("<MouseWheel>", self.zooming)
        self.zget = self.zoom_slider.get()

    def zooming(self, event):
        try:
            self.preview_window.deiconify()
            xcord = event.x
            ycord = event.y
            self.zget = self.zoom_slider.get()
            # if event.delta > 0:
            #     self.zoom_slider.set(self.zget + 0.5)
            # elif event.delta < 0:
            #     self.zoom_slider.set(self.zget - 0.5)
            self.lim = (100 // self.zget)
            t3img = self.t1img.crop((xcord - self.lim, ycord - self.lim, xcord + self.lim, ycord + self.lim))
            t4img = ctk.CTkImage(t3img, size=(400, 400))
            self.prv_lbl.configure(image=t4img)
            self.preview_window.lift()
        except:
            self.preview_action()

    def display_image(self, image=None):
        self.canvas.delete("all")
        if image is None:
            image = self.edited_img.copy()

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channels = image.shape
        ratio = height / width

        new_width = width
        new_height = height

        if height > 800 or width > 1200:
            if ratio < 1:
                new_width = 1200
                new_height = int(new_width * ratio)
            else:
                new_height = 800
                new_width = int(new_height * (width / height))

        self.ratio = height / new_height
        self.new_image = cv2.resize(image, (new_width, new_height))

        self.new_image = ImageTk.PhotoImage(
            Image.fromarray(self.new_image))

        self.canvas.config(width=new_width, height=new_height)
        self.canvas.create_image(
            new_width / 2, new_height / 2, image=self.new_image)

# import intropagev1
app1 = ctk.CTk()
app1.configure(bg_color="black", fg_color="black")
PhotoEdit1(app=app1)

app1.mainloop()
