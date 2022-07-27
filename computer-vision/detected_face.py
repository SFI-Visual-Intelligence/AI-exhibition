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

        # Choose the index of the closest rectangle
        choice = np.argmin(distances)

        # Store a tuple of the combination of indices
        matches.append((i, indexes[choice]))

        # Remove previous choice
        indexes = np.delete(indexes, choice)

        # Iterate till rectangle_list2 is exhausted.
        if len(indexes) == 0:
            break
    
    return matches 

def face_analyzing(img, face_pos):
    """Function that estimates age, gender and emotion of face. Additionally orders data 
    following other face recognition.

    Inputs are the frame of intrest and the position of the box framing the 
    faces found by the other face recognition in shape of [(x1,y1,w1,h1), (x2,y2,w2,h2)]

    Returns:
        Dictionary of estimates of age, gender and emotion, and list of faces found ordered
    """
    # Finds faces within frame.
    faces_found = RetinaFace.extract_faces(img)
    
    # Estimates age, gender and emotion of face found.
    estimation = DeepFace.analyze(faces_found, actions = ['age', 'gender', 'emotion'], enforce_detection=False) 
    
    # Instantiate object for each face
    faces = [AnalyzedFace(face_attributes) for _, face_attributes in estimation.items()]

    face_analyed_pos = [face.rect for face in faces]
    # print(estimation)
    # for face in estimation: #fetches the position of the faces found by retina
        # face_analyed_pos.append((estimation[face]['region']['x'], estimation[face]['region']['y'], estimation[face]['region']['w'], estimation[face]['region']['h']))


    """
    Output of function currently gives ordered_faces=['instance_1'] should modify to 
    take order into class then output its order as an attribute to the class. could also possibly
    shorten the code for rectangle_comparison as some can be done within class methods.
    """

    #finds which data correponds with which face
    matching_faces = rectangle_comparison(face_pos, face_analyed_pos)

    estimated_faces = []    
    for face in estimation: 
        estimated_faces.append(face)
    
    #reorders faces to correspond
    ordered_faces = []
    for (i,j) in matching_faces:
        ordered_faces.append(estimated_faces[j])

    print(ordered_faces, 'Ordered faces')
    
    return estimation, ordered_faces



class AnalyzedFace:
    """
    Analyzed face object.
    """

    def __init__(self, face):
        self.face = face
        print(self.face)
        self._x, self._y, self._w, self._h = map(int, self.face["region"].values())
        self._gender = self.face["gender"]
        self._emotion = self.face["dominant_emotion"]
        self._center = self.get_center(self.x, self.y, self.w, self.h)

    @property
    def rect(self):
        return (self.x, self.y, self.w, self.h)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def w(self):
        return self._w

    @property
    def h(self):
        return self._h

    @property
    def center(self):
        return self._center

    @property
    def gender(self):
        return self._gender

    @property
    def emotion(self):
        return self._emotion

    @staticmethod
    def get_center(x, y, w, h):
        return np.array([x, y]) + np.array([w // 2, h // 2])

    def __str__(self):
        return f"x={self.x}, y={self.y}, w={self.w}, h={self.h}, center={self.center}, gender={self.gender}, emotion={self.emotion}"
    

if __name__ == '__main__':
    rects1 = [(1, 1, 1, 1), (1.5, 1.5, 1, 1), (-1, 0, 2.1, 2)]
    rects2 = [(3, 3, 1, 1), (2, 2, 1, 1), (5, 3, 1.5, 1.5)]

    print(rectangle_comparison(rects1, rects2))
