from realesrgan_ncnn_py import Realesrgan
from upscale_ncnn_py import UPSCALE
from realcugan_ncnn_py import Realcugan
from PIL import Image
#13
upscale1 = UPSCALE(gpuid=0,model=21,num_threads=2)

with Image.open("Pasted image.png") as image:
    
        image = upscale1.process_pil(image)

image.save("output1.png", quality=95)