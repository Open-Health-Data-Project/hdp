# Team 4
import PIL.Image
import PIL.ImageDraw
import face_recognition
import cv2

def recognize_face(file):
    # Load the jpg file into a numpy array
    image = face_recognition.load_image_file(file)

    # Find all the faces in the image
    face_locations = face_recognition.face_locations(image)

    number_of_faces = len(face_locations)
    print("I found {} face(s) in this photograph.".format(number_of_faces))

    # Load the image into a Python Image Library object so that we can draw on top of it and display it
    #pil_image = PIL.Image.fromarray(image)
    image_output = cv2.imread(file)
    image_marked=image_output.copy()
    directory = "recognized_faces\\"
    counter=1

    for face_location in face_locations:

        # Print the location of each face in this image. Each face is a list of co-ordinates in (top, right, bottom, left) order.
        top, right, bottom, left = face_location
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

        # Let's draw a box around the face
        margin = (bottom - top)//2
        window_name="Znalezione"
        top=top-margin-(margin//2)
        left=left-margin
        bottom=bottom+margin
        right=right+margin
        start_point = (left,top)
        end_point = (right,bottom)
        color = (0,0,255)
        thickness = 2
        image_marked= cv2.rectangle(image_marked, start_point, end_point, color, thickness)

        crop_img = image_output[top:bottom, left:right].copy()

        cv2.imwrite(directory+str(counter)+".jpg", crop_img)
        counter+=1
        #draw = PIL.ImageDraw.Draw(pil_image)
        #draw.rectangle([left, top, right, bottom], outline="red")

    # Display the image on screen
    #pil_image.show()
    cv2.imshow(window_name, image_marked)
    cv2.waitKey()

recognize_face("people.jpg")
