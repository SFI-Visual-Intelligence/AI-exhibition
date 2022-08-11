import cv2

def getIntegers(string):
  numbers = [int(x) for x in string.split() if x.isnumeric()]
  return numbers[0]
  
def chosen_option():
    choice = input('Enter the number of the style you want: ')

    return getIntegers(choice)