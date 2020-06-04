# Team 4
import cv2
import glob
import uuid

# e.g. frames_per_seconds = 2 means 2 images per 1 second
def create_animation(frames_per_second=0.8):
    path_images = "recognized_faces_animation/*.jpg"
    # Creating the unique animation title.
    animation_title = str(uuid.uuid4()) + ".mp4"
    animation_size = (640, 480)

    # Creating list for images at a given face_composition.
    image_array = []
    for image_file in glob.glob(path_images):
        image = cv2.imread(image_file)
        image_array.append(image)
        print(image_file)

    animation = cv2.VideoWriter(animation_title, cv2.VideoWriter_fourcc(*"mp4v"), frames_per_second, animation_size)

    for item in image_array:
        # write() includes only the images that have the same size as has been specified when opening the video writer
        animation.write(item)

    animation.release()

    return animation


mp4_animation = create_animation()
