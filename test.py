#from realesrgan_ncnn_py import Realesrgan
from realcugan_ncnn_py import Realcugan
from upscale_ncnn_py import UPSCALE
import cv2

import numpy as np#13 
import tqdm
#upscale1 = UPSCALE(gpuid=0,num_threads=2,model_str="/home/pax/.local/share/REAL-Video-Enhancer/models/realesrgan/models/realesr-animevideov3-x4",scale=4) #<- shufflecugan
#upscale1 = UPSCALE(model=13,num_threads=2)
upscale1 = UPSCALE(gpuid=0,num_threads=2,scale=2,models_path="/home/pax/.local/share/REAL-Video-Enhancer/models/realcugan/",model="models-se") #<- shufflecugan
image = cv2.imdecode(np.fromfile("input.png", dtype=np.uint8), cv2.IMREAD_COLOR)
'''for i in tqdm.tqdm(range(100)):
    upscale1.process_cv2(image)'''
upscale1.process_cv2(image)
image.save("output.png", quality=95)