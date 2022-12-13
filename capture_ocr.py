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
    capture_decoder_return = 0.00
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

            matchespi = matchespi[0].split() 
            for pulsatility_index in matchespi:
                try:
                    float(pulsatility_index)
                    capture_decoder_return = pulsatility_index
                    break
                except ValueError:
                    #print("Value Error; not a float")
                    pulsatility_index = "Not a Float"
            
            return(capture_decoder_return)

        elif array_lengthvf != 0:

            #print(matchesvf)
            matchesvf = matchesvf[0].split() 
            for volume_flow in matchesvf:
                try:
                    float(volume_flow)
                    capture_decoder_return = volume_flow
                    break
                except ValueError:
                    #print("Value Error; not a float")
                    volume_flow = "Not a Float"            
            return(capture_decoder_return)

        else:
            return(capture_decoder_return)

if __name__ == "__main__":
    return_val = capture_decoder()
    #logging.info
    print("return_val = ", return_val)