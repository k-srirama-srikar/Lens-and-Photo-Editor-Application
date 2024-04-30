# Lens-and-Photo-Editor-Application

### By:
- [Kakaraparty Srirama Srikar (142301013)](https://github.com/k-srirama-srikar)
- [Kallakuri Venkata Surya Bharath (112301013)](https://github.com/BharathKallakuri)
- [Pentakota Narayana Chanakya (102301027)](https://github.com/ChanakyaPKD)
<br>

### About:
Our application Lens and Photo Editor brings together enchanting live Snapchat-like lenses and a very convinient photo editor with a wide range of image manipulation tools to use providing you with an application that can help you make or take visually appealing images.

<br>

### Getting started:
Run the following to install OpenCV, numpy, Pillow, Customtkinter, Mediapipe (Note that Mediapipe is compatible for versions of python less than 3.11.9)
<br>
```
pip install opencv-python
pip install numpy
pip install pillow
pip install customtkinter
pip install mediapipe
```
<br>
After installing the required, you can proceed to download the zip file.
<br>
After downloading and extracting the zip file from the repository, open the directory in command prompt and type the following command to run `homepage.py` :
<br>

- Windows:
```
python homepage.py
```
<br>

- LINUX / MacOS:
```
python3 homepage.py
```

<br>

### How to use:
The homepage provides you with a welcome screen and two button-like images to choose from - Lens or Editor.<br>
Clicking either of them will take you to the respective programs.<br><br>
Lens: <br>
On opening it, you will see a camera-like application, with various buttons. You can play around with the filters and take good images of yourself.<br><br>
Editor:<br>
The editor asks you to upload an image initially. After uploading, you'll see a variety fratures being displayed. You can use all of them to make the image look better.

<br>

### Implementations:
- We used Python based library Customtkinter and Python library Tkinter for the GUI.
- To get the live feed from camera or make changes to an image, we have used OpenCV.
- For facial feature detection, we used the Python based library MediaPipe.
- We have used Pillow as well to change a few properties of images.

<br>

### Contributions:
1. Kakaraparty Srirama Srikar:<br>
• Created the layout of GUI in the Photo Lens Application.<br>
• Created Crop, Draw, Add Text and Apply Filter functions
in the Photo Editor Application.<br>
• Created the Overlay function for different lenses in the
Photo Lens Application.<br><br>
2. Kallakuri Venkata Surya Bharath:<br>
• Created the layout of GUI in the Photo Editor Application.<br>
• Created the preview function in Photo Editor Application.<br>
• Designed the Introductory Window and its corresponding
functions.<br><br>
3. Pentakota Narayana Chanakya:<br>
• Created Undo button, Redo buttons and corresponding
functions for every action in the Photo Editor Application.<br>
• Created the Adjust option functions and Blurring
functions in Photo Editor Application.<br>
• Created the lenses in the Photo Editor Application.

<br>

### License
This project is licensed under the MIT License. 
