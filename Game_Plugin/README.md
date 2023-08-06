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
