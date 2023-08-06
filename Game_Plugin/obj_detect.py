# Load YOLOv8n, train it on COCO128 for 3 epochs and predict an image with it
from ultralytics import YOLO
import cv2
import os
import argparse

def load_model():
    return None

class Detector:
    def __init__(self, m=None):
        self.m = YOLO('yolov8n.pt' if not m else m)
        # self.m.to('cuda')
    
    # return list of objects in img in the form of [class, x, y, w, h, conf]
    def inference_img(self,img):
        results = self.m.predict(source=img, verbose=False, device=0)
        return results[0].boxes.cpu().numpy()   
    
    def train(self,data=None):
        model = self.m
        # Use the model
        model.train(data="coco128.yaml", epochs=3)  # train the model
        metrics = model.val()  # evaluate model performance on the validation set
        results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image
        path = model.export(format="engine")  # export the model to ONNX format

# run this file for test purpose
def display_dataset():
    im2 = cv2.imread("D:/Hack/Game-CV-Simu/Game_Plugin/data/datasets/test/images/r5apex_23-04-2019_21-06-21-84_003955_crp_0.jpg")
    print(im2.shape)
    with open("D:/Hack/Game-CV-Simu/Game_Plugin/data/datasets/test/labels/r5apex_23-04-2019_21-06-21-84_003955_crp_0.txt", 'r') as f:
        # print(f.read())
        window_size = 648
        obj = f.read().split()
        
        x,y = float(obj[1]) * window_size, float(obj[2]) * window_size
        w,h = float(obj[3]) * window_size, float(obj[4]) * window_size
        x1,y1 = int(x-w/2), int(y-h/2)
        cv2.rectangle(im2, (x1,y1), (int(x1+w),int(y1+h)), (0, 0, 255), 2)
    while True:
        cv2.imshow('OpenCV/Numpy normal', im2)
        if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        
def predict_one_img(m=None):
    dt = Detector(m)
    # m.train()
    im2 = cv2.imread("D:/Hack/Game-CV-Simu/Game_Plugin/data/datasets/test/images/r5apex_23-04-2019_21-06-21-84_003955_crp_0.jpg")
    print(im2.shape)
    results = dt.m.predict(source=im2, device=0)  # save predictions as labels
    print(results[0].boxes.cpu().numpy()[0].cls)
    
    # for result in results:                                         # iterate results
    #     boxes = result.boxes.cpu().numpy()                         # get boxes on cpu in numpy
    #     for box in boxes:                                          # iterate boxes
    #         r = box.xyxy[0].astype(int)                            # get corner points as int
    #         print(r)                                               # print boxes
    #         cv2.rectangle(im2, r[:2], r[2:], (255, 255, 255), 2)   # draw boxes on img
    # while True:
    #     cv2.imshow('OpenCV/Numpy normal', im2)
    #     if cv2.waitKey(25) & 0xFF == ord('q'):
    #             cv2.destroyAllWindows()
    #             break
    
def main(model):
    print(model)
    for i in range(1):
        predict_one_img(model)
    # m = YOLO('best.pt')
    # m.to('cuda')
    # path = m.export(format="engine", device=0)
    # print(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default=None, help='Model to predict.')
    args = parser.parse_args()
    main(args.model)