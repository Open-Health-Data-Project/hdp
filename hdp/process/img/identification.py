import face_recognition

def identify_person(source_img, compare_img):
    # Load the known images
    image_of_person_1 = face_recognition.load_image_file(source_img)

    # Get the face encoding of each person. This can fail if no one is found in the photo.
    person_1_face_encoding = face_recognition.face_encodings(image_of_person_1)[0]

    # Create a list of all known face encodings
    known_face_encodings = [
        person_1_face_encoding,
    ]

    # Load the image we want to check - as in example compare_img="unknown8.jpg"
    unknown_image = face_recognition.load_image_file(compare_img)

    # Get face encodings for any people in the picture
    face_locations = face_recognition.face_locations(unknown_image, number_of_times_to_upsample=2)
    unknown_face_encodings = face_recognition.face_encodings(unknown_image, known_face_locations=face_locations)

    # There might be more than one person in the photo, so we need to loop over each face we found
    for unknown_face_encoding in unknown_face_encodings:

        # Test if this unknown face encoding matches any of the three people we know
        results = face_recognition.compare_faces(known_face_encodings, unknown_face_encoding, tolerance=0.6)

        name = "Unknown"

        if results[0]:
            name = "Person"
            print(f"Found {name} in the photo!")
            return True
    print("Person not found")
    return False