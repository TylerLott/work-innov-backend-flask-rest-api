# TODO write overview
# TODO finish class
import cv2
import os
import numpy
import pytesseract
import pandas as pd
import numpy as np
# from calamari_ocr.ocr.predict.predictor import MultiPredictor, PredictorParamsM

if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class OCR:
    def __init__(self, image):
        self.image = image
        self.bitnot = image
        self.boxes = []
        self.countcol = 0
        self.rowcount = 0

    def get_rois(self):
        thresh,img_bin = cv2.threshold(self.image,128,255,cv2.THRESH_BINARY |cv2.THRESH_OTSU)
        img_bin = 255-img_bin

        # get vertical and horizontal lines
        kernel_len = np.array(self.image).shape[1]//25
        ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
        hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

        #vertical 
        image_1 = cv2.erode(img_bin, ver_kernel, iterations=3)
        vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)

        #horizontal
        image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
        horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)

        #combine
        img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
        img_vh = cv2.erode(~img_vh, kernel, iterations=2)
        thresh, img_vh = cv2.threshold(img_vh,128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        bitxor = cv2.bitwise_xor(self.image,img_vh)
        self.bitnot = cv2.bitwise_not(bitxor)

        contours, hierarchy = cv2.findContours(img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Sort all the contours by top to bottom.
        contours, boundingBoxes = self.__sort_contours(contours, method="ttb")
    
        #Creating a list of heights for all detected boxes
        heights = [boundingBoxes[i][3] for i in range(len(boundingBoxes))]
        #Get mean of heights
        mean = np.mean(heights)

        #Create list box to store all boxes in  
        box = []
        # Get position (x,y), width and height for every contour and show the contour on image
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if (w<1000 and h<500):
                image = cv2.rectangle(self.image,(x,y),(x+w,y+h),(0,255,0),2)
                pad = 1
                box.append([x,y,w-pad,h])

        #Creating two lists to define row and column in which cell is located
        row=[]
        column=[]
        j=0
        #Sorting the boxes to their respective row and column
        for i in range(len(box)):
            if(i==0):
                column.append(box[i])
                previous=box[i]
            else:
                if(box[i][1]<=previous[1]+mean/2):
                    column.append(box[i])
                    previous=box[i]
                    if(i==len(box)-1):
                        row.append(column)
                else:
                    row.append(column)
                    column=[]
                    previous = box[i]
                    column.append(box[i])

        self.rowcount = len(row)
        self.countcol = 0
        for i in range(len(row)):
            self.countcol = len(row[i])
            if self.countcol > self.countcol:
                self.countcol = self.countcol

        center = [int(row[i][j][0]+row[i][j][2]/2) for j in range(len(row[i])) if row[0]]
        center=np.array(center)
        center.sort()

        finalboxes = []
        for i in range(len(row)):
            lis=[]
            for k in range(self.countcol):
                lis.append([])
            for j in range(len(row[i])):
                diff = abs(center-(row[i][j][0]+row[i][j][2]/4))
                minimum = min(diff)
                indexing = list(diff).index(minimum)
                lis[indexing].append(row[i][j])
            finalboxes.append(lis)
        self.boxes = finalboxes


    def extract(self):
        outer=[]
        # counter = 0
        for i in range(len(self.boxes)):
            for j in range(len(self.boxes[i])):
                inner=''
                if(len(self.boxes[i][j])==0):
                    outer.append('')
                else:
                    for k in range(len(self.boxes[i][j])):
                        y,x,w,h = self.boxes[i][j][k][0],self.boxes[i][j][k][1], self.boxes[i][j][k][2],self.boxes[i][j][k][3]
                        finalimg = self.bitnot[x:x+h, y:y+w]
                        cv2.imwrite('final.png', finalimg)

                        
                        out = pytesseract.image_to_data(finalimg, lang="eng", config='-c tessedit_char_whitelist=" 01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.-/" --psm 6 --oem 1', output_type=pytesseract.Output.DICT)
                        # counter +=1
                        # print("############### boxes",self.boxes[i][j])
                        # if counter > 3:
                        #     pass
                        #     # fds
                        ind = np.where(np.array(out.get('conf')) != '-1')
                        text = ''
                        conf = 0
                        if len(ind[0]) > 1:
                            for n in ind[0]:
                                text = text + out.get('text')[n] + ' '
                                conf += float(out.get('conf')[n])
                        elif len(ind[0]) == 1:
                            text = out.get('text')[ind[0][0]]
                            conf = float(out.get('conf')[ind[0][0]])

                        conf = conf / len(ind[0])
                        # print(text)

                        inner = [text, conf]
                    outer.append(inner)


        arr = np.array(outer)
        print(arr)
        return arr.reshape((self.rowcount,self.countcol, 2)).tolist()
        # dataframe = pd.DataFrame(arr.reshape((self.rowcount,self.countcol, 2)))
        # return dataframe.to_json(orient="values")

    def __sort_contours(self, cnts, method="ltr"):
        # initialize the reverse flag and sort index
        reverse = False
        i = 0
        # handle if we need to sort in reverse
        if method == "rtl" or method == "btt":
            reverse = True
        # handle if we are sorting against the y-coordinate rather than
        # the x-coordinate of the bounding box
        if method == "ttb" or method == "btt":
            i = 1
        # construct the list of bounding boxes and sort them from top to
        # bottom
        boundingBoxes = [cv2.boundingRect(c) for c in cnts]
        (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
        key=lambda b:b[1][i], reverse=reverse))
        # return the list of sorted contours and bounding boxes
        return (cnts, boundingBoxes)


if __name__ == "__main__":
    img = cv2.imread('../../test_image_5.png',0)
    ocr = OCR(img)
    ocr.get_rois()
    data = ocr.extract()
    print(data)