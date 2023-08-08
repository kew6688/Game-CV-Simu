# Apex Legends Aim Assit

## Design
- ### Screen Shot: 
    win32gui lib.
    Achieve 300 FPS.
- ### Inference: 
    Using YOLOv8n. 
    Trained with custom dataset (7000+ images, 30 epo). 
    export to tensorrt ('.engine'). 'best.pt' 10ms => 'best.engine' 4ms
    Achieve 80 FPS.
- ### Simulation:
    Using pynput as listener
    Using pydirectinput for in-game input
  
### Game -> screen_grab -> obj_detect -> simul_control
multiprocessing: one process handles game-play inference; sencond process handles keyboard listener and mouse input in game

![Diagram](gp.png)

## Run
``` python main.py ```
main program start point. 
args: '--test' output real-time inference images with bounding boxes

``` python screen_grab.py ```
get active window. Passing window title to screen shot function could increase FPS

``` python obj_detect.py ```
single image detection and model export

``` train.ipynb ```
train YOLO model, start with pre-trained yolov8n.pt

## Performance
### Screen Shots
    Several popular python screen shots method are tested. Performance for 10 shots are listed:
        - pil time: 18.548096656799316 FPS: 0.5391388768903264
        - win32 time: 0.46700000762939453 FPS: 21.413275881433982
        - PyQt time: 0.08246302604675293 FPS: 121.26646910010842
        Both win32 and PyQt are implemented and can be switched in main program.

### Inference
    Predict on GPU achieve 15ms on average. 
    By export model to TensorRT (".engine"), the inference time is less than 4ms on average.
    
## TODO
pynput listener causing a lagging during gameplay. May due to poor CPU.
