import numpy as np
from retinaface import RetinaFace
from deepface import DeepFace

def vec(x,y):
    return np.array([x,y])

def rectangle_comparison(rectangle_list1, rectangle_list2):
    """Function that compares two lists of rectangles.

    Lists are ordered as rectangle_list1: [(x1,y1,w1,h1), (x2,y2,w2,h2)]

    Returns:
        list(Tuple(index from rectangle_list1, index from rectangle_list2), Tuple(another index from rectangle_list1, another index from rectangle_list2))
    """

    # list to store matching rectangles
    matches = []

    indexes = np.arange(len(rectangle_list2))
    # iterating over coordinates of first list of rectangles
    # print(rectangle_list1)
    for i, (x1,y1,w1,h1) in enumerate(rectangle_list1):

        # List for storing calculated distances
        distances = []

        # Finding the center coordinate of the rectangle
        center1 = vec(x1,y1) + vec(w1 // 2, h1 // 2)

        # 
        for j in indexes:
            print(rectangle_list2[j])
            (x2, y2, w2, h2)=rectangle_list2[j]
            center2 = vec(x2, y2) + vec(w2 // 2, h2 // 2)

            dist = np.linalg.norm(center1 - center2)
            distances.append(dist)

        # Iterating over second rectangle list
        # for (x2,y2,w2,h2) in rectangle_list2:

        #     # Center of second rectangles
        #     center2 = vec(x2,y2) + vec(w2 // 2, h2 // 2)

        #     # Calculate distance between centers
        #     dist = np.linalg.norm(center1 - center2)
        #     distances.append(dist)

        # Choose the index of the closest rectangle
        choice = np.argmin(distances)

        # Store a tuple of the combination of indices
        matches.append((i, indexes[choice]))

        # Remove previous choice
        indexes = np.delete(indexes, choice)
        # print(indexes, choice)


        # Iterate till rectangle_list2 is exhausted.
        if len(indexes) == 0:
            break
    
    return matches 

def face_analyzing(img, face_pos):
    """Function that estimates age, gender and emotion of face. Additionally orders data following other face recognition

    Inputs are the frame of intrest and the position of the box framing the faces found by the other face recognition in shape of [(x1,y1,w1,h1), (x2,y2,w2,h2)]

    Returns:
        Dictionary of estimates of age, gender and emotion, and list of faces found ordered
    """
    #finds faces within frame
    faces_found = RetinaFace.extract_faces(img)
    
    #estimates age, gender and emotion of face found
    estimation = DeepFace.analyze(faces_found, actions = ['age', 'gender', 'emotion'], enforce_detection=False) 
    
    face_analyed_pos = []
    # print(estimation)
    for face in estimation: #fetches the position of the faces found by retina
        face_analyed_pos.append((estimation[face]['region']['x'], estimation[face]['region']['y'], estimation[face]['region']['w'], estimation[face]['region']['h']))
    matching_faces = rectangle_comparison(face_pos, face_analyed_pos)   #finds which data correponds with which face
    estimated_faces = []    
    for face in estimation: 
        estimated_faces.append(face)
    
    ordered_faces = []
    for (i,j) in matching_faces:    #reorders faces to correspond
        ordered_faces.append(estimated_faces[j])

    print(ordered_faces, 'Ordered faces')
    
    return estimation, ordered_faces


    

# identified = [Face(person_id, analyzed_dict) for person_id, analyzed_dict in zip()]

class Face:
    def __init__(self, person_id, analyzed_dict):
        pass


    

if __name__ == '__main__':
    rects1 = [(1, 1, 1, 1), (1.5, 1.5, 1, 1), (-1, 0, 2.1, 2)]
    rects2 = [(3, 3, 1, 1), (2, 2, 1, 1), (5, 3, 1.5, 1.5)]

    print(rectangle_comparison(rects1, rects2))
