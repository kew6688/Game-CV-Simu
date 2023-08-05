# # Load YOLOv8n, train it on COCO128 for 3 epochs and predict an image with it
# from ultralytics-main.ultralytics import YOLO

# model = YOLO('yolov8n.pt')  # load a pretrained YOLOv8n detection model
# model.train(data='coco128.yaml', epochs=3)  # train the model
# model('https://ultralytics.com/images/bus.jpg')  # predict on an image

def load_model():
    return None

class Detector:
    # def __init__(self, m=None):
        # self.m = YOLO('yolov8n.pt' if not m else m)
    
    def inference_img(self,img):
        return []
    
    # def train(self,data=None):
    #     model = self.m
    #     # Use the model
    #     model.train(data="coco128.yaml", epochs=3)  # train the model
    #     metrics = model.val()  # evaluate model performance on the validation set
    #     results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image
    #     path = model.export(format="eigen")  # export the model to ONNX format

# run this file for training purpose
def main():
    m = Detector()
    m.train()

if __name__ == "__main__":
    main()