from realesrgan_ncnn_py import Realesrgan
from realcugan_ncnn_py import Realcugan
from upscale_ncnn_py import UPSCALE
from PIL import Image
#13 
upscale1 = UPSCALE(gpuid=0,num_threads=2,model_str="/home/pax/.local/share/REAL-Video-Enhancer/models/realesrgan/models/realesr-animevideov3-x4",scale=4) #<- shufflecugan
#upscale1 = UPSCALE(model=1)
with Image.open("input.png") as image:
    image = upscale1.process_pil(image)

image.save("output.png", quality=95)