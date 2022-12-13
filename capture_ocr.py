import cv2 as cv
import pytesseract
from PIL import Image
import logging

def capture_from_image():
    cap = cv.VideoCapture(0)
    while cap.isOpened():
        
        ret, frame = cap.read()

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
   
        cap.release()
        cv.destroyAllWindows()
        return gray

def capture_decoder():
    searching_for_text = True
    while searching_for_text:
        img1 = capture_from_image()
        text = pytesseract.image_to_string(Image.fromarray(img1))

        split_txt = text.split("\n")
        logging.info("found data: %s", split_txt)
        matchespi = [match for match in split_txt if "PI" in match]
        matchesvf = [match for match in split_txt if "Vol Flow" in match]
        array_lengthpi = len(matchespi)
        array_lengthvf = len(matchesvf)


        if array_lengthpi != 0:

            for i in range(array_lengthpi):
                matchespi[i] = ",".join( matchespi[i].split() )
                #print(matchespi)
                #print("sent pi to alg: ", matchespi)
                return(matchespi)

        elif array_lengthvf != 0:

            for i in range(array_lengthvf):
                matchesvf[i] = ",".join( matchesvf[i].split() )
                #print(matchesvf)
                #print("sent vf to alg: ", matchesvf)
                return(matchesvf)
        else:
            print("no data found")

if __name__ == "__main__":
    capture_decoder()