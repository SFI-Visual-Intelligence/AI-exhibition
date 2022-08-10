import numpy as np
from retinaface import RetinaFace
from deepface import DeepFace

def vec(x,y):
    """
    Function which creates numpy 2-d vector.

    Args
    ----
    x: int
    y: int

    Returns
    -------
    ndarray(x,y)
    """

    return np.array([x,y])

def get_center(x, y, w, h):
    """
    Find center of rectangle.

    Args
    ----
    x, y, w, g: int

    Returns
    -------
    ndarray
        Vector representing center of rectangle.
    """

    return vec(x, y) + vec(w // 2, h // 2)

def rectangle_comparison(rectangle_list1, rectangle_list2):
    """Function that compares two lists of rectangles.

    Lists are ordered as rectangle_list1: [(x1,y1,w1,h1), (x2,y2,w2,h2)]

    Args
    ----
    rectangle_list1: list
        First list of rectangles.
    rectangle_list2: list
        Second list of rectangles.

    Returns
    -------
    list(Tuple(index from rectangle_list1, index from rectangle_list2), Tuple(another index from rectangle_list1, another index from rectangle_list2))
    """

    # list to store matching rectangles
    matches = []

    indexes = np.arange(len(rectangle_list2))

    # iterating over coordinates of first list of rectangles
    for i, (x1,y1,w1,h1) in enumerate(rectangle_list1):

        # List for storing calculated distances
        distances = []

        # Finding the center coordinate of the rectangle
        center1 = get_center(x1, y1, w1, h1)

        # Iterating over second lists rectangles
        for j in indexes:

            # Find centers of rectangles
            (x2, y2, w2, h2)=rectangle_list2[j]
            center2 = get_center(x2, y2, w2, h2)

            # Distance measure from each center of first list to each center of second list
            dist = np.linalg.norm(center1 - center2)
            distances.append(dist)
        # print(distances)

        # Choose the index of the closest rectangle
        choice = np.argmin(distances)
        # print(person_ids)

        # Store a tuple of the combination of indices
        matches.append(indexes[choice])
    

        # Remove previous choice
        indexes = np.delete(indexes, choice)
        # indexes1 = np.delete(indexes1, 0)
        # person_ids = np.delete(person_ids, i)

        # Iterate till rectangle_list2 or rectangle_list1 is exhausted.
        if len(indexes) == 0:
            break
    
    return matches 

def face_analyzing(img, haar_faces):
    """Function that estimates age, gender and emotion of face. Additionally orders data 
    following other face recognition.

    Inputs are the frame of intrest and the position of the box framing the 
    faces found by the other face recognition in shape of [(x1,y1,w1,h1), (x2,y2,w2,h2)]

    Returns:
        Dictionary of estimates of age, gender and emotion, and list of faces found ordered
    """
    # Finds faces within frame.
    # faces_found = RetinaFace.extract_faces(img)
    # print('RetinaFace:', type(faces_found[0]), faces_found[0].shape)
    # raise
    faces_found = []
    
    for face in haar_faces:
        x, y, w, h = face
        faces_found.append(img[int(x*2/3):int(x*2/3 + w*3/2), int(y*2/3):int(y*2/3 + h*3/2)])
        
    # Estimates age, gender and emotion of face found.
    estimation = DeepFace.analyze(faces_found, actions = ['age', 'gender', 'emotion'], enforce_detection=False) 
    
    # Instantiate object for each face
    faces = [AnalyzedFace(face_attributes) for _, face_attributes in estimation.items()]
    for ind, face in enumerate(faces):
        face.x, face.y, face.w, face.h = haar_faces[ind]

    # face_analyed_pos = [face.rect for face in faces]
    # print(estimation)
    # for face in estimation: #fetches the position of the faces found by retina
        # face_analyed_pos.append((estimation[face]['region']['x'], estimation[face]['region']['y'], estimation[face]['region']['w'], estimation[face]['region']['h']))


    """
    Output of function currently gives ordered_faces=['instance_1'] should modify to 
    take order into class then output its order as an attribute to the class. could also possibly
    shorten the code for rectangle_comparison as some can be done within class methods.
    """

    # Finds what data correponds to which face
    # matching_faces = rectangle_comparison(face_pos, face_analyed_pos)
    # print(matching_faces)
    

    ### Uncomment for DEBUGGING
    # for face in faces: print(face)

    return faces

class AnalyzedFace:
    """
    Analyzed face object.
    """

    def __init__(self, face):
        self.face = face
        self.x, self.y, self.w, self.h = map(int, self.face["region"].values())
        self._gender = self.face["gender"]
        self._emotion = self.face["dominant_emotion"]
        self._age = self.face["age"]
        self._name = None
        self._center = self.get_center(self.x, self.y, self.w, self.h)
        self._haarcascade_id = None
        self._deepface_id = None



    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def haarcascade_id(self):
        return self._haarcascade_id

    @property
    def deepface_id(self):
        return self._deepface_id

    @haarcascade_id.setter
    def haarcascade_id(self, h_id):
        self._haarcascade_id = h_id

    @deepface_id.setter
    def deepface_id(self, d_id):
        self._deepface_id = d_id

    @property
    def rect(self):
        return (self.x, self.y, self.w, self.h)


    @property
    def center(self):
        return self._center

    @property
    def gender(self):
        return self._gender

    @property
    def emotion(self):
        return self._emotion

    @property
    def age(self):
        return self._age

    @staticmethod
    def get_center(x, y, w, h):
        return np.array([x, y]) + np.array([w // 2, h // 2])

    def __str__(self):
        return f"x={self.x}, y={self.y}, w={self.w}, h={self.h}, center={self.center}, gender={self.gender}, emotion={self.emotion}, age={self.age}, h_id={self.haarcascade_id}, d_id={self.deepface_id}"

    def __repr__(self):
        return f"x={self.x}, y={self.y}, w={self.w}, h={self.h}, center={self.center}, gender={self.gender}, emotion={self.emotion}, age={self.age}, h_id={self.haarcascade_id}, d_id={self.deepface_id}"
    

if __name__ == '__main__':
    rects1 = [(1, 1, 1, 1), (1.5, 1.5, 1, 1), (-1, 0, 2.1, 2)]
    rects2 = [(3, 3, 1, 1), (2, 2, 1, 1), (5, 3, 1.5, 1.5)]

    print(rectangle_comparison(rects1, rects2))
