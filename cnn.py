import cv2
import imutils
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


image = cv2.imread("8.jpeg") 


if image is None:
    print("Error: Unable to load the image.")
else:
    
    image = imutils.resize(image, width=500)
    
  
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    edges = cv2.Canny(gray, 170, 200)

    # Find contours in the edged image
    cnts, _ = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

  
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    NumberPlateCnt = None

    # Loop over the contours
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            NumberPlateCnt = approx
            x, y, w, h = cv2.boundingRect(c)
            new_img = image[y:y + h, x:x + w]
            cv2.imwrite('Cropped_image.png', new_img)  # Save the cropped image
            break

    # Perform OCR on the cropped number plate image
    Cropped_img_loc = 'Cropped_image.png'
    text = pytesseract.image_to_string(Cropped_img_loc, lang='eng')


    print("Recognized Number Plate:", text)

   
    lines = text.split('\n')
    print("Individual Lines:")
    for line in lines:
        print(line)
