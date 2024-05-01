import customtkinter as ctk
import cv2
import numpy as np
from PIL import Image, ImageTk
import threading
from tkinter import filedialog, colorchooser, ROUND
from datetime import datetime
import mediapipe as mp
import itertools

# from playsound import playsound
# import pixellib as pb

# initializing mediapipe face detection class
mp_face_detection = mp.solutions.face_detection

# setting up face detection function
face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

# mediapipe drawing class
mp_drawing = mp.solutions.drawing_utils

# mediapipe face mesh class
mp_face_mesh = mp.solutions.face_mesh

# mediapipe drawing styles class
mp_drawing_styles = mp.solutions.drawing_styles

face_mesh_videos = mp_face_mesh.FaceMesh(static_image_mode=False,
                                         max_num_faces=5,
                                         min_detection_confidence=0.5,
                                         min_tracking_confidence=0.3)


# here the maximum number of faces is taken as 5 initially, but we can continuously track them
# by using len(face_detection_results.detections)


class VideoStreamWidget(ctk.CTkLabel):
    def __init__(self, master=None, video_source=0):
        super().__init__(master)
        self.configure(text="")
        self.video_source = video_source
        self.video_stream = cv2.VideoCapture(self.video_source)
        width, height = 1280, 720
        self.video_stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.val = 0
        self.video_stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.thread = threading.Thread(target=self.update_video_stream, daemon=True)
        self.thread.start()
        self.mesh_display_value = 0
        self.glow_fire_value = 0
        self.straw_hat_val = 0
        self.straw_hat_img = cv2.imread("media/mugi12.png")
        self.glow_fire_left_eye = cv2.imread("media/Lighting-removebg-preview.png")
        self.glow_fire_right_eye = cv2.imread("media/Lighting-removebg-preview.png")
        self.glow_fire_smoke_animation = cv2.VideoCapture("media/smoke_animation.mp4")
        self.glow_fire_smoke_frame_counter = 0
        self.sunglasses_val = 0
        self.sunglasses_img = cv2.imread("media/sunglasses2.png")
        self.cap_val = 0
        self.cap_imp = cv2.imread("media/poke_hats.png")

    def update_video_stream(self):
        while True:
            self.ret, self.frame = self.video_stream.read()
            self.frame = cv2.flip(self.frame, flipCode=1)

            if self.ret:
                if self.val == 1:
                    cv2.putText(self.frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (20, 690),
                                2, 0.5,
                                (255, 255, 0))

                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

                if self.mesh_display_value == 1:
                    self.frame, _ = self.detectFacialLandmarks(self.frame, face_mesh_videos, display=False)

                if self.glow_fire_value == 1:
                    _, smoke_frame = self.glow_fire_smoke_animation.read()

                    self.glow_fire_smoke_frame_counter += 1

                    if self.glow_fire_smoke_frame_counter == self.glow_fire_smoke_animation.get(
                            cv2.CAP_PROP_FRAME_COUNT):
                        # Set the current frame position to first frame to restart the video.
                        self.glow_fire_smoke_animation.set(cv2.CAP_PROP_POS_FRAMES, 0)

                        # Set the smoke animation video frame counter to zero.
                        self.glow_fire_smoke_frame_counter = 0

                    _, face_mesh_results = self.detectFacialLandmarks(self.frame, face_mesh_videos, display=False)

                    if face_mesh_results.multi_face_landmarks:
                        mouth_status = self.isOpen(self.frame, face_mesh_results, "MOUTH",
                                                   threshold=15, display=False)
                        # Get the left eye isOpen status of the person in the frame.
                        left_eye_status = self.isOpen(self.frame, face_mesh_results, 'LEFT EYE',
                                                      threshold=4, display=False)

                        # Get the right eye isOpen status of the person in the frame.
                        right_eye_status = self.isOpen(self.frame, face_mesh_results, 'RIGHT EYE',
                                                       threshold=4, display=False)

                        for face_num, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):
                            # Check if the left eye of the face is open.
                            if left_eye_status[face_num] == 'OPEN':
                                # Overlay the left eye image on the frame at the appropriate location.
                                self.frame = self.overlay(self.frame, self.glow_fire_left_eye, face_landmarks,
                                                          'LEFT EYE', mp_face_mesh.FACEMESH_LEFT_EYE, display=False)

                            # Check if the right eye of the face is open.
                            if right_eye_status[face_num] == 'OPEN':
                                # Overlay the right eye image on the frame at the appropriate location.
                                self.frame = self.overlay(self.frame, self.glow_fire_right_eye, face_landmarks,
                                                          'RIGHT EYE', mp_face_mesh.FACEMESH_RIGHT_EYE, display=False)

                                # Check if the mouth of the face is open.
                            if mouth_status[face_num] == 'OPEN':
                                # Overlay the smoke animation on the frame at the appropriate location.
                                self.frame = self.overlay(self.frame, smoke_frame, face_landmarks,
                                                          'MOUTH', mp_face_mesh.FACEMESH_LIPS, display=False)

                if self.straw_hat_val == 1:
                    _, face_mesh_results = self.detectFacialLandmarks(self.frame, face_mesh_videos, display=False)

                    if face_mesh_results.multi_face_landmarks:
                        face_status = self.isOpen(self.frame, face_mesh_results, 'FACE',
                                                  threshold=5, display=False)
                        for face_num, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):
                            if face_status:
                                self.frame = self.mugi_overlay(self.frame, self.straw_hat_img[:, :, ::-1],
                                                               face_landmarks,
                                                               'FACE', mp_face_mesh.FACEMESH_FACE_OVAL,
                                                               display=False)

                if self.sunglasses_val == 1:
                    _, face_mesh_results = self.detectFacialLandmarks(self.frame, face_mesh_videos, display=False)

                    if face_mesh_results.multi_face_landmarks:

                        # # Get the left eye isOpen status of the person in the frame.
                        nose_status = self.isOpen(self.frame, face_mesh_results, 'NOSE',
                                                  threshold=5, display=False)
                        for face_num, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):
                            if nose_status:
                                self.frame = self.glasses_overlay(self.frame, self.sunglasses_img[:, :, ::-1],
                                                                  face_landmarks,
                                                                  'NOSE', mp_face_mesh.FACEMESH_NOSE,
                                                                  display=False)

                if self.cap_val == 1:
                    _, face_mesh_results = self.detectFacialLandmarks(self.frame, face_mesh_videos, display=False)

                    if face_mesh_results.multi_face_landmarks:

                        # # Get the left eye isOpen status of the person in the frame.
                        face_status = self.isOpen(self.frame, face_mesh_results, 'FACE',
                                                  threshold=5, display=False)
                        for face_num, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):
                            if face_status:
                                self.frame = self.cap_overlay(self.frame, self.cap_imp[:, :, ::-1], face_landmarks,
                                                              'FACE', mp_face_mesh.FACEMESH_FACE_OVAL,
                                                              display=False)

                image = Image.fromarray(self.frame)
                photo = ImageTk.PhotoImage(image=image)
                self.configure(image=photo)
                self.image = photo
                self.neu_frame = self.frame

    def detectFacialLandmarks(self, image, face_mesh, display=True):
        results = face_mesh.process(image)

        self.output_image = image.copy()

        if results.multi_face_landmarks:

            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(image=self.output_image,
                                          landmark_list=face_landmarks,
                                          connections=mp_face_mesh.FACEMESH_TESSELATION,
                                          landmark_drawing_spec=None)


                mp_drawing.draw_landmarks(image=self.output_image, landmark_list=face_landmarks,
                                          connections=mp_face_mesh.FACEMESH_CONTOURS,
                                          landmark_drawing_spec=None,
                                          connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())

        return np.ascontiguousarray(self.output_image, dtype=np.uint8), results

    def stop(self):
        # self.video_stream.release()

        original_file_type = "jpg"
        saved_image = self.neu_frame[:, :, ::-1]
        filename = filedialog.asksaveasfilename()
        filename = filename + "." + original_file_type
        # saved_image = self.frame
        # saved_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        cv2.imwrite(filename, saved_image)
        self.filename = filename
        self.video_stream.read()
        # self.video_stream.release()

    def filter_none(self):
        self.mesh_display_value = 0
        self.glow_fire_value = 0
        self.straw_hat_val = 0
        self.sunglasses_val = 0
        self.cap_val = 0

    def timestamp(self):
        self.val = 1
        cv2.putText(self.frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (20, 30), cv2.FONT_HERSHEY_DUPLEX, 0.5,
                    (0, 255, 255))

    def mesh_display(self):
        self.mesh_display_value = 1
        self.glow_fire_value = 0
        self.sunglasses_val = 0
        self.cap_val = 0
        self.straw_hat_val = 0

    def mugi_disp(self):
        self.mesh_display_value = 0
        self.glow_fire_value = 0
        self.straw_hat_val = 1
        self.sunglasses_val = 0
        self.cap_val = 0

    def apple_display(self):
        self.mesh_display_value = 0
        self.glow_fire_value = 0
        self.straw_hat_val = 0
        self.sunglasses_val = 1
        self.cap_val = 0

    def poke_hat_display(self):
        self.mesh_display_value = 0
        self.glow_fire_value = 0
        self.straw_hat_val = 0
        self.sunglasses_val = 0
        self.cap_val = 1

    def remtimestamp(self):
        self.val = 0

    def fire_display(self):
        self.glow_fire_value = 1
        self.mesh_display_value = 0
        self.straw_hat_val = 0
        self.sunglasses_val = 0
        self.cap_val = 0

    def getSize(self, image, face_landmarks, INDEXES):
        '''
        This function calculate the height and width of a face part utilizing its landmarks.
        Args:
            image:          The image of person(s) whose face part size is to be calculated.
            face_landmarks: The detected face landmarks of the person whose face part size is to
                            be calculated.
            INDEXES:        The indexes of the face part landmarks, whose size is to be calculated.
        Returns:
            width:     The calculated width of the face part of the face whose landmarks were passed.
            height:    The calculated height of the face part of the face whose landmarks were passed.
            landmarks: An array of landmarks of the face part whose size is calculated.
        '''

        # Retrieve the height and width of the image.
        image_height, image_width, _ = image.shape

        # Convert the indexes of the landmarks of the face part into a list.
        INDEXES_LIST = list(itertools.chain(*INDEXES))

        # Initialize a list to store the landmarks of the face part.
        landmarks = []

        # Iterate over the indexes of the landmarks of the face part.
        for INDEX in INDEXES_LIST:
            # Append the landmark into the list.
            landmarks.append([int(face_landmarks.landmark[INDEX].x * image_width),
                              int(face_landmarks.landmark[INDEX].y * image_height)])

        # Calculate the width and height of the face part.
        _, _, width, height = cv2.boundingRect(np.array(landmarks))

        # Convert the list of landmarks of the face part into a numpy array.
        landmarks = np.array(landmarks)

        # Return the calculated width height and the landmarks of the face part.
        return width, height, landmarks

    def isOpen(self, image, face_mesh_results, face_part, threshold=5, display=True):
        '''
        This function checks whether the an eye or mouth of the person(s) is open,
        utilizing its facial landmarks.
        Args:
            image:             The image of person(s) whose an eye or mouth is to be checked.
            face_mesh_results: The output of the facial landmarks detection on the image.
            face_part:         The name of the face part that is required to check.
            threshold:         The threshold value used to check the isOpen condition.
            display:           A boolean value that is if set to true the function displays
                               the output image and returns nothing.
        Returns:
            output_image: The image of the person with the face part is opened  or not status written.
            status:       A dictionary containing isOpen statuses of the face part of all the
                          detected faces.
        '''

        # Retrieve the height and width of the image.
        image_height, image_width, _ = image.shape

        # Create a copy of the input image to write the isOpen status.
        output_image = image.copy()

        # Create a dictionary to store the isOpen status of the face part of all the detected faces.
        status = {}

        # Check if the face part is mouth.
        if face_part == 'MOUTH':
            # Get the indexes of the mouth.
            INDEXES = mp_face_mesh.FACEMESH_LIPS


        elif face_part == "NOSE":
            INDEXES = mp_face_mesh.FACEMESH_NOSE

        elif face_part == "FACE":
            INDEXES = mp_face_mesh.FACEMESH_FACE_OVAL

        # Check if the face part is left eye.
        elif face_part == 'LEFT EYE':
            # Get the indexes of the left eye.
            INDEXES = mp_face_mesh.FACEMESH_LEFT_EYE

        # Check if the face part is right eye.

        elif face_part == 'RIGHT EYE':

            # Get the indexes of the right eye.
            INDEXES = mp_face_mesh.FACEMESH_RIGHT_EYE

        # Otherwise return nothing.

        else:
            return

        # Iterate over the found faces.
        for face_no, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):

            # Get the height of the face part.
            _, height, _ = self.getSize(image, face_landmarks, INDEXES)

            # Get the height of the whole face.
            _, face_height, _ = self.getSize(image, face_landmarks, mp_face_mesh.FACEMESH_FACE_OVAL)

            # Check if the face part is open.
            if (height / face_height) * 100 > threshold:

                # Set status of the face part to open.
                status[face_no] = 'OPEN'

            # Otherwise.
            else:
                # Set status of the face part to close.
                status[face_no] = 'CLOSE'

        # Returns the isOpen statuses of the face part of each detected face.
        return status

    def overlay(self, image, filter_img, face_landmarks, face_part, INDEXES, display=True):

        annotated_image = image.copy()
        try:

            # Get the width and height of filter image.
            filter_img_height, filter_img_width, _ = filter_img.shape

            # Get the height of the face part on which we will overlay the filter image.
            _, face_part_height, landmarks = self.getSize(image, face_landmarks, INDEXES)

            # Specify the height to which the filter image is required to be resized.
            required_height = int(face_part_height * 3)

            # Resize the filter image to the required height, while keeping the aspect ratio constant.
            resized_filter_img = cv2.resize(filter_img, (int(filter_img_width *
                                                             (required_height / filter_img_height)),
                                                         required_height))



            # Get the new width and height of filter image.
            filter_img_height, filter_img_width, _ = resized_filter_img.shape

            # Convert the image to grayscale and apply the threshold to get the mask image.
            _, filter_img_mask = cv2.threshold(cv2.cvtColor(resized_filter_img, cv2.COLOR_BGR2GRAY),
                                               25, 255, cv2.THRESH_BINARY_INV)

            # Calculate the center of the face part.
            center = landmarks.mean(axis=0).astype("int")

            # Check if the face part is mouth.
            if face_part == 'MOUTH':

                # Calculate the location where the smoke filter will be placed.
                location = (int(center[0] - filter_img_width / 3), int(center[1]))

            # Otherwise if the face part is an eye.
            else:

                # Calculate the location where the eye filter image will be placed.
                location = (int(center[0] - filter_img_width / 2), int(center[1] - filter_img_height / 2))

            # Retrieve the region of interest from the image where the filter image will be placed.
            ROI = image[location[1]: location[1] + filter_img_height,
                  location[0]: location[0] + filter_img_width]

            # Perform Bitwise-AND operation. This will set the pixel values of the region where,
            # filter image will be placed to zero.
            resultant_image = cv2.bitwise_and(ROI, ROI, mask=filter_img_mask)

            # Add the resultant image and the resized filter image.
            # This will update the pixel values of the resultant image at the indexes where
            # pixel values are zero, to the pixel values of the filter image.
            resultant_image = cv2.add(resultant_image, resized_filter_img)

            # Update the image's region of interest with resultant image.
            annotated_image[location[1]: location[1] + filter_img_height,
            location[0]: location[0] + filter_img_width] = resultant_image

            # Catch and handle the error(s).
        except Exception as e:
            pass

        # Return the annotated image.
        return annotated_image

    def mugi_overlay(self, image, filter_img, face_landmarks, face_part, INDEXES, display=True):

        annotated_image = image.copy()
        try:

            # Get the width and height of filter image.
            filter_img_height, filter_img_width, _ = filter_img.shape

            # Get the height of the face part on which we will overlay the filter image.
            face_part_width, face_part_height, landmarks = self.getSize(image, face_landmarks, INDEXES)

            # Specify the height to which the filter image is required to be resized.
            required_height = int(face_part_height * 0.9)

            # Resize the filter image to the required height, while keeping the aspect ratio constant.
            resized_filter_img = cv2.resize(filter_img, (int(filter_img_width *
                                                             (required_height / filter_img_height)),
                                                         required_height))



            # Get the new width and height of filter image.
            filter_img_height, filter_img_width, _ = resized_filter_img.shape

            # Convert the image to grayscale and apply the threshold to get the mask image.
            _, filter_img_mask = cv2.threshold(cv2.cvtColor(resized_filter_img, cv2.COLOR_BGR2GRAY),
                                               25, 255, cv2.THRESH_BINARY_INV)

            # Calculate the center of the face part.
            center = landmarks.mean(axis=0).astype("int")

            # Check if the face part is mouth.
            if face_part == 'FACE':

                # Calculate the location where the smoke filter will be placed.
                location = (int(center[0] - filter_img_width / 2),
                            int(center[1] - face_part_height - filter_img_height / 4))

            elif face_part == 'NOSE':
                location = (int(center[0] - filter_img_width / 2), int(center[1] - filter_img_height / 2))

            # Otherwise if the face part is an eye.
            else:

                # Calculate the location where the eye filter image will be placed.
                location = (int(center[0] - filter_img_width / 2), int(center[1] - filter_img_height / 2))

            # Retrieve the region of interest from the image where the filter image will be placed.
            ROI = image[location[1]: location[1] + filter_img_height,
                  location[0]: location[0] + filter_img_width]

            # Perform Bitwise-AND operation. This will set the pixel values of the region where,
            # filter image will be placed to zero.
            resultant_image = cv2.bitwise_and(ROI, ROI, mask=filter_img_mask)

            # Add the resultant image and the resized filter image.
            # This will update the pixel values of the resultant image at the indexes where
            # pixel values are zero, to the pixel values of the filter image.
            resultant_image = cv2.add(resultant_image, resized_filter_img)

            # Update the image's region of interest with resultant image.
            annotated_image[location[1]: location[1] + filter_img_height,
            location[0]: location[0] + filter_img_width] = resultant_image

            # Catch and handle the error(s).
        except Exception as e:
            pass

        # Return the annotated image.
        return annotated_image


    def glasses_overlay(self, image, filter_img, face_landmarks, face_part, INDEXES, display=True):


        annotated_image = image.copy()
        try:

            # Get the width and height of filter image.
            filter_img_height, filter_img_width, _ = filter_img.shape

            # Get the height of the face part on which we will overlay the filter image.
            face_part_width, face_part_height, landmarks = self.getSize(image, face_landmarks, INDEXES)

            # Specify the height to which the filter image is required to be resized.
            required_width = int(face_part_width * 4)

            # Resize the filter image to the required height, while keeping the aspect ratio constant.
            resized_filter_img = cv2.resize(filter_img, (int(required_width),
                                                         int(filter_img_height * (required_width / filter_img_width))))



            # Get the new width and height of filter image.
            filter_img_height, filter_img_width, _ = resized_filter_img.shape

            # Convert the image to grayscale and apply the threshold to get the mask image.
            _, filter_img_mask = cv2.threshold(cv2.cvtColor(resized_filter_img, cv2.COLOR_BGR2GRAY),
                                               25, 255, cv2.THRESH_BINARY_INV)

            # Calculate the center of the face part.
            center = landmarks.mean(axis=0).astype("int")

            # Check if the face part is mouth.
            # if face_part == 'MOUTH':
            #
            #     # Calculate the location where the smoke filter will be placed.
            #     location = (int(center[0] - filter_img_width / 3), int(center[1]))

            if face_part == 'NOSE':
                location = (int(center[0] - filter_img_width / 2), int(center[1] - face_part_height))

            # Otherwise if the face part is an eye.
            else:

                # Calculate the location where the eye filter image will be placed.
                location = (int(center[0] - filter_img_width / 2), int(center[1] - filter_img_height / 2))

            # Retrieve the region of interest from the image where the filter image will be placed.
            ROI = image[location[1]: location[1] + filter_img_height,
                  location[0]: location[0] + filter_img_width]

            # Perform Bitwise-AND operation. This will set the pixel values of the region where,
            # filter image will be placed to zero.
            resultant_image = cv2.bitwise_and(ROI, ROI, mask=filter_img_mask)

            # Add the resultant image and the resized filter image.
            # This will update the pixel values of the resultant image at the indexes where
            # pixel values are zero, to the pixel values of the filter image.
            resultant_image = cv2.add(resultant_image, resized_filter_img)

            # Update the image's region of interest with resultant image.
            annotated_image[location[1]: location[1] + filter_img_height,
            location[0]: location[0] + filter_img_width] = resultant_image

            # Catch and handle the error(s).
        except Exception as e:
            pass

        # Return the annotated image.
        return annotated_image

    def cap_overlay(self, image, filter_img, face_landmarks, face_part, INDEXES, display=True):

        annotated_image = image.copy()
        try:

            # Get the width and height of filter image.
            filter_img_height, filter_img_width, _ = filter_img.shape

            # Get the height of the face part on which we will overlay the filter image.
            face_part_width, face_part_height, landmarks = self.getSize(image, face_landmarks, INDEXES)

            # Specify the height to which the filter image is required to be resized.
            required_height = int(face_part_height)

            # Resize the filter image to the required height, while keeping the aspect ratio constant.
            resized_filter_img = cv2.resize(filter_img, (int(filter_img_width *
                                                             (required_height / filter_img_height) * 1.2),
                                                         required_height))

            # overlay for eyepatch

            # # Specify the height to which the filter image is required to be resized.
            # required_height = int(face_part_height * 3)
            #
            # # Resize the filter image to the required height, while keeping the aspect ratio constant.
            # resized_filter_img = cv2.resize(filter_img, (int(filter_img_width *
            #                                                  (required_height / filter_img_height)*2),
            #                                              required_height))

            # Get the new width and height of filter image.
            filter_img_height, filter_img_width, _ = resized_filter_img.shape

            # Convert the image to grayscale and apply the threshold to get the mask image.
            _, filter_img_mask = cv2.threshold(cv2.cvtColor(resized_filter_img, cv2.COLOR_BGR2GRAY),
                                               25, 255, cv2.THRESH_BINARY_INV)

            # Calculate the center of the face part.
            center = landmarks.mean(axis=0).astype("int")

            # Check if the face part is mouth.
            if face_part == 'FACE':

                # Calculate the location where the smoke filter will be placed.
                location = (int(center[0] - filter_img_width / 2),
                            int(center[1] - face_part_height - filter_img_height / 4))

            elif face_part == 'NOSE':
                location = (int(center[0] - filter_img_width / 2), int(center[1] - filter_img_height / 2))

            # Otherwise if the face part is an eye.
            else:

                # Calculate the location where the eye filter image will be placed.
                location = (int(center[0] - filter_img_width / 2), int(center[1] - filter_img_height / 2))

            # Retrieve the region of interest from the image where the filter image will be placed.
            ROI = image[location[1]: location[1] + filter_img_height,
                  location[0]: location[0] + filter_img_width]

            # Perform Bitwise-AND operation. This will set the pixel values of the region where,
            # filter image will be placed to zero.
            resultant_image = cv2.bitwise_and(ROI, ROI, mask=filter_img_mask)

            # Add the resultant image and the resized filter image.
            # This will update the pixel values of the resultant image at the indexes where
            # pixel values are zero, to the pixel values of the filter image.
            resultant_image = cv2.add(resultant_image, resized_filter_img)

            # Update the image's region of interest with resultant image.
            annotated_image[location[1]: location[1] + filter_img_height,
            location[0]: location[0] + filter_img_width] = resultant_image

            # Catch and handle the error(s).
        except Exception as e:
            pass

        # Return the annotated image.
        return annotated_image


class CustomTkinterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Photo Lens")
        self.after(0, lambda: self.state("zoomed"))
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.configure(bg_color="black", fg_color="black")
        # self.app.state('zoomed')
        # app.state("zoomed")
        self.iconbitmap("media/lenico.ico")
        self.video_widget = VideoStreamWidget(self)
        # self.video_widget.pack(padx=20, pady=20)
        self.video_widget.place(relx=0.4, rely=0.5, anchor="center")

        self.home_logo = ctk.CTkImage(light_image=Image.open("media/home button.png"),
                                      dark_image=Image.open("media/home button.png"),
                                      size=(20, 20))
        self.editor_btn = ctk.CTkButton(master=self, text='', width=20, corner_radius=0, bg_color='black',
                                        fg_color='transparent',
                                        image=self.home_logo, command=self.home_page, hover_color="#242424")
        self.editor_btn.place(relx=0.0, rely=0.0, anchor="nw")

        self.date_time_check_box = ctk.CTkCheckBox(master=self, text="Add timestamp", command=self.dtstamp,
                                                   hover_color="#ff7400", fg_color="#ffad00")
        self.date_time_check_box.place(relx=0.06, rely=0.94, anchor="sw")

        # self.stop_button = ctk.CTkButton(self, text="Stop", command=self.stop_video_stream)
        # self.stop_button.pack(padx=20, pady=10)
        self.capture_button = ctk.CTkButton(master=self, width=100, height=100, corner_radius=50, text="",
                                            hover_color="#c9c8c7",
                                            command=self.stop_video_stream, border_width=5, border_color="gray",
                                            fg_color="white")
        self.capture_button.place(relx=0.95, rely=0.5, anchor="center")

        mesh_img = ctk.CTkImage(light_image=Image.open("media/mesh_buttonp (1).png"),
                                dark_image=Image.open("media/mesh_buttonp (1).png"),
                                size=(40, 50))
        fire_img = ctk.CTkImage(light_image=Image.open("media/blue_transparent_fire2.png"),
                                dark_image=Image.open("media/blue_transparent_fire2.png"),
                                size=(40, 50))
        straw_hat_mugiwara_img = ctk.CTkImage(light_image=Image.open("media/mugiwara.png"),
                                  dark_image=Image.open("media/mugiwara.png"),
                                  size=(40, 50))
        apple_img = ctk.CTkImage(light_image=Image.open("media/sunglasses2.png"),
                                 dark_image=Image.open("media/sunglasses2.png"),
                                 size=(40, 25))
        cap_img = ctk.CTkImage(light_image=Image.open("media/poke_hats.png"),
                               dark_image=Image.open("media/poke_hats.png"),
                               size=(40, 50))
        no_filter_img = ctk.CTkImage(light_image=Image.open("media/none2.png"),
                                     dark_image=Image.open("media/none2.png"),
                                     size=(40, 40))

        self.mesh_button = ctk.CTkButton(master=self, width=80, height=80, corner_radius=40, text="",
                                         hover_color="#242424", image=mesh_img,
                                         command=self.mesh_disp, border_width=3, border_color="#ffad00",
                                         fg_color="black")
        self.mesh_button.place(relx=0.95, rely=0.35, anchor="center")

        self.fire_button = ctk.CTkButton(master=self, width=80, height=80, corner_radius=40, text="",
                                         hover_color="#242424", image=fire_img,
                                         command=self.fire_disp, border_width=3, border_color="#ffad00",
                                         fg_color="black")
        self.fire_button.place(relx=0.95, rely=0.07, anchor="center")

        self.mugi_button = ctk.CTkButton(master=self, width=80, height=80, corner_radius=40, text="",
                                         hover_color="#242424", image=straw_hat_mugiwara_img,
                                         command=self.straw_hat, border_width=3, border_color="#ffad00",
                                         fg_color="black")
        self.mugi_button.place(relx=0.95, rely=0.21, anchor="center")

        self.apple_button = ctk.CTkButton(master=self, width=80, height=80, corner_radius=40, text="",
                                          hover_color="#242424", image=apple_img,
                                          command=self.apple, border_width=3, border_color="#ffad00",
                                          fg_color="black")
        self.apple_button.place(relx=0.95, rely=0.79, anchor="center")

        self.cap_button = ctk.CTkButton(master=self, width=80, height=80, corner_radius=40, text="",
                                        hover_color="#242424", image=cap_img,
                                        command=self.ash_cap, border_width=3, border_color="#ffad00",
                                        fg_color="black")
        self.cap_button.place(relx=0.95, rely=0.65, anchor="center")

        self.none_button = ctk.CTkButton(master=self, width=80, height=80, corner_radius=40, text="",
                                         hover_color="#242424", image=no_filter_img,
                                         command=self.no_fun, border_width=3, border_color="#ffad00",
                                         fg_color="black")
        self.none_button.place(relx=0.95, rely=0.93, anchor="center")

    def home_page(self):
        self.destroy()
        import homepage
        try:
            homepage.app.mainloop()
        except:
            homepage.app = ctk.CTk()
            homepage.app.mainloop()

    def stop_video_stream(self):
        self.video_widget.stop()

    def no_fun(self):
        self.video_widget.filter_none()

    def mesh_disp(self):
        self.video_widget.mesh_display()

    def apple(self):
        self.video_widget.apple_display()

    def ash_cap(self):
        self.video_widget.poke_hat_display()

    def fire_disp(self):
        self.video_widget.fire_display()

    def straw_hat(self):
        self.video_widget.mugi_disp()

    def dtstamp(self):
        value = self.date_time_check_box.get()
        if value == 1:
            self.video_widget.timestamp()
        else:
            self.video_widget.remtimestamp()


def start_lens():
    app2 = CustomTkinterApp()

    app2.mainloop()


start_lens()
