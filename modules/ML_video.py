#made by Sherwin Maharjan
from ultralytics import YOLO
import cv2 as cv
import numpy as np
from math import sqrt

class VRS():
    NO_MAX_IMG = -1
    
    def __init__(self, model_loc:str, scale:int=0.5, limit:int=2):
        self.scale = scale
        self.model = YOLO(model_loc)
        self.limit = limit
        
    def __call__(self):
        return self.img
    
    def __str__(self) -> str:
        return "VRS activated"
    
    def predict(self, img:np.array, img_flip:bool=True,device:str="mps"):
        if img_flip:
            self.img = cv.flip(img, 1)
        else:
            self.img = img
        self.shape = img.shape
        self.resize_dim = (int(img.shape[1]*self.scale), int(img.shape[0]*self.scale))
        self.resize = cv.resize(self.img, self.resize_dim, cv.INTER_AREA)
        self.abcd = []
        self.predicted_items = []
        
        results= self.model.predict(source=self.resize, conf=0.5, device=device, stream=True)
        
        for r in results:
            boxes = r.boxes.xywh.cpu().numpy().astype(int)
            classes = r.boxes.cls.cpu().numpy().astype(int)

            for (x, y, w, h), cls in zip(boxes, classes):
                self.abcd.append((x - w // 2, y - h // 2, x + w // 2, y + h // 2))
                self.predicted_items.append(r.names[cls])
        
        return self.abcd, self.predicted_items
    
    def plot(self):
        inlarge = lambda x:int(x/self.scale)
        
        for cords, items in zip(self.abcd[:self.limit], self.predicted_items[:self.limit]):
            a, b, c, d = map(inlarge, cords)
            cv.rectangle(self.img, (a, b), (c,d), (0, 255, 0), 2)
            cv.putText(self.img , items, (a, d), cv.FONT_HERSHEY_TRIPLEX, 2, (0, 255, 0), 2)
            
        return self.img

    def add_img(self, png):
        for i in self.abcd[:self.limit]:
            dst = (int(i[0]*2),int(i[1]*2))
            loc =  (int((i[2]-i[0])*2), int((i[3]-i[1])*2))
            scale_factor = min(loc[0] / png.shape[0], loc[1] / png.shape[1])
            new_width = int(png.shape[1] * scale_factor)
            new_height = int(png.shape[0] * scale_factor)
            
            png_resized = cv.resize(png, (new_width, new_height), interpolation=cv.INTER_AREA)
            for i, a in enumerate(range(dst[1], dst[1] + png_resized.shape[0])):
                for j, b in enumerate(range(dst[0], dst[0] + png_resized.shape[1])):
                    if 0 <= a < self.img.shape[0] and 0 <= b < self.img.shape[1]:  
                        if png_resized[i, j].all() != 0: 
                            self.img[a, b] = png_resized[i, j]
            
        return self.img
    
    @property
    def mid_coords(self):
        self.m_coords = []
        for i in self.abcd:
            m_coord = (int((i[2]+i[0])/2), int((i[3]+i[1])/2))
            self.m_coords.append(m_coord)
        return self.m_coords
    
    @property
    def max_obj(self):
        if not self.abcd:
            return None

        distances = [sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) for x1, y1, x2, y2 in self.abcd]
        max_index = np.argmax(distances)

        return self.mid_coords[max_index] if distances else None
            
            
        
def main():
    cap = cv.VideoCapture(0)
    vr = VRS(model_loc="./ML_algorithm/yolo11n.pt", limit=10)
    while True:
        suc, frame = cap.read()
        abcd, items = vr.predict(frame, img_flip=True)
        img = vr.plot()
        cv.imshow("VRS", img)
        print(vr.max_obj)
        if cv.waitKey(1) == ord("q"):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()