from realesrgan_ncnn_py import Realesrgan
from upscale_ncnn_py import UPSCALE

from PIL import Image

upscale1 = UPSCALE(gpuid=0,model=15)
with Image.open("input.png") as image:
    image = upscale1.process_pil(image)
    image.save("output.jpg", quality=95)