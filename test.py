from realesrgan_ncnn_py import Realesrgan
from upscale_ncnn_py import Span

from PIL import Image

upscale = Span(gpuid=0,model=4)
with Image.open("input.png") as image:
    image = upscale.process_pil(image)
    image.save("output.jpg", quality=95)