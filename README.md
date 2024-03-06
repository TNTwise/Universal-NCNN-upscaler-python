# upscale-ncnn-py
 


### Custom SPAN models:
- <a href="https://openmodeldb.info/models/4x-ClearRealityV1">ClearRealityV1 (4X)</a> by Kim2091
- <a href="https://github.com/terrainer/AI-Upscaling-Models/tree/main/4xSPANkendata">SPANkendata (4X)</a> by terrainer
- <a href="https://github.com/Phhofm/models"> 2xHFA2kSpan (2x)</a> by Phhofm <br/>
https://openmodeldb.info/models/2x-sudo-shuffle-cugan-9-584-969 <br/>
Python Binding for upscale-ncnn-py with PyBind11

[![PyPI version](https://badge.fury.io/py/realesrgan-ncnn-py.svg?123456)](https://badge.fury.io/py/realesrgan-ncnn-py?123456)
[![test_pip](https://github.com/Final2x/realesrgan-ncnn-py/actions/workflows/test_pip.yml/badge.svg)](https://github.com/Final2x/realesrgan-ncnn-py/actions/workflows/test_pip.yml)
[![Release](https://github.com/Tohrusky/realesrgan-ncnn-py/actions/workflows/Release.yml/badge.svg)](https://github.com/Tohrusky/realesrgan-ncnn-py/actions/workflows/Release.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/upscale-ncnn-py)

Span go brrr for upscaling images.

### Current building status matrix

|    System     |                                                                                                               Status                                                                                                                | CPU (32bit) |    CPU (64bit)     | GPU (32bit) |    GPU (64bit)     |
| :-----------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :---------: | :----------------: | :---------: | :----------------: |
| Linux (Clang) |         [![CI-Linux-x64-Clang](https://github.com/Tohrusky/realesrgan-ncnn-py/actions/workflows/CI-Linux-x64-Clang.yml/badge.svg)](https://github.com/Tohrusky/realesrgan-ncnn-py/actions/workflows/CI-Linux-x64-Clang.yml)         |      —      | :white_check_mark: |      —      | :white_check_mark: |
|  Linux (GCC)  |            [![CI-Linux-x64-GCC](https://github.com/Tohrusky/realesrgan-ncnn-py/actions/workflows/CI-Linux-x64-GCC.yml/badge.svg)](https://github.com/Tohrusky/realesrgan-ncnn-py/actions/workflows/CI-Linux-x64-GCC.yml)            |      —      | :white_check_mark: |      —      | :white_check_mark: |
|    Windows    |       [![CI-Windows-x64-MSVC](https://github.com/Tohrusky/upscale-ncnn-py/actions/workflows/CI-Windows-x64-MSVC.yml/badge.svg)](https://github.com/Tohrusky/upscale-ncnn-py/actions/workflows/CI-Windows-x64-MSVC.yml)        |      —      | :white_check_mark: |      —      | :white_check_mark: |
|     MacOS     | [![CI-MacOS-Universal-Clang](https://github.com/Tohrusky/realcugan-ncnn-py/actions/workflows/CI-MacOS-Universal-Clang.yml/badge.svg)](https://github.com/Tohrusky/realcugan-ncnn-py/actions/workflows/CI-MacOS-Universal-Clang.yml) |      —      | :white_check_mark: |      —      | :white_check_mark: |
|  MacOS (ARM)  | [![CI-MacOS-Universal-Clang](https://github.com/Tohrusky/realcugan-ncnn-py/actions/workflows/CI-MacOS-Universal-Clang.yml/badge.svg)](https://github.com/Tohrusky/realcugan-ncnn-py/actions/workflows/CI-MacOS-Universal-Clang.yml) |      —      | :white_check_mark: |      —      | :white_check_mark: |

# Usage

`Python >= 3.6 (>= 3.9 in MacOS arm)`

To use this package, simply install it via pip:

```sh
pip install upscale-ncnn-py
```

For Linux user:

```sh
apt install -y libomp5 libvulkan-dev
cd /usr/lib
sudo ln -s libomp.so libomp.so.5
```

Then, import the upscale class from the package:

```python
from upscale_ncnn_py import UPSCALE
```

To initialize the model:

```python
upscale = UPSCALE(gpuid: int = 0, tta_mode: bool = False, tilesize: int = 0, model: int = 0)
# model can be 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19; 0 for default
#span
0: {"param": "spanx2_ch48.param", "bin": "spanx2_ch48.bin", "scale": 2, "folder": "models/SPAN"},
1: {"param": "spanx2_ch52.param", "bin": "spanx2_ch52.bin", "scale": 2, "folder": "models/SPAN"},
2: {"param": "spanx4_ch48.param", "bin": "spanx4_ch48.bin", "scale": 4, "folder": "models/SPAN"},
3: {"param": "spanx4_ch52.param", "bin": "spanx4_ch52.bin", "scale": 4, "folder": "models/SPAN"},
#custom span
4: {"param": "2xHFA2kSPAN_27k.param", "bin": "2xHFA2kSPAN_27k.bin", "scale": 2, "folder": "models/SPAN"},
5: {"param": "4xSPANkendata.param", "bin": "4xSPANkendata.bin", "scale": 4, "folder": "models/SPAN"},
6: {"param": "ClearReality4x.param", "bin": "ClearReality4x.bin", "scale": 4, "folder": "models/SPAN"},

#esrgan
7: {"param": "realesr-animevideov3-x2.param", "bin": "realesr-animevideov3-x2.bin", "scale": 2, "folder": "models/ESRGAN"},
8: {"param": "realesr-animevideov3-x3.param", "bin": "realesr-animevideov3-x3.bin", "scale": 3, "folder": "models/ESRGAN"},
9: {"param": "realesr-animevideov3-x4.param", "bin": "realesr-animevideov3-x4.bin", "scale": 4, "folder": "models/ESRGAN"},
10: {"param": "realesrgan-x4plus-x4.param", "bin": "realesrgan-x4plus.bin", "scale": 4, "folder": "models/ESRGAN"},
11: {"param": "realesrgan-x4plus-anime.param", "bin": "realesrgan-x4plus-anime.bin", "scale": 4, "folder": "models/ESRGAN"},

#cugan-se models 
12: {"param": "up2x-conservative.param", "bin": "up2x-conservative.bin", "scale": 2, "folder": "models/CUGAN/models-se"},
13: {"param": "up2x-no-denoise.param", "bin": "up2x-no-denoise.bin", "scale": 2, "folder": "models/CUGAN/models-se"},
14: {"param": "up2x-denoise1x.param", "bin": "up2x-denoise1x.bin", "scale": 2, "folder": "models/CUGAN/models-se"},
15: {"param": "up2x-denoise2x.param", "bin": "up2x-denoise2x.bin", "scale": 2, "folder": "models/CUGAN/models-se"},
16: {"param": "up2x-denoise3x.param", "bin": "up2x-denoise3x.bin", "scale": 2, "folder": "models/CUGAN/models-se"},

17: {"param": "up3x-conservative.param", "bin": "up3x-conservative.bin", "scale": 3, "folder": "models/CUGAN/models-se"},
18: {"param": "up3x-no-denoise.param", "bin": "up3x-no-denoise.bin", "scale": 3, "folder": "models/CUGAN/models-se"},
19: {"param": "up3x-denoise3x.param", "bin": "up3x-denoise3x.bin", "scale": 3, "folder": "models/CUGAN/models-se"},

20: {"param": "up4x-conservative.param", "bin": "up4x-conservative.bin", "scale": 4, "folder": "models/CUGAN/models-se"},
21: {"param": "up4x-no-denoise.param", "bin": "up4x-no-denoise.bin", "scale": 4, "folder": "models/CUGAN/models-se"},
22: {"param": "up4x-denoise3x.param", "bin": "up3x-denoise3x.bin", "scale": 4, "folder": "models/CUGAN/models-se"},

#cugan-pro models
23: {"param": "up2x-denoise3x.param", "bin": "up2x-denoise3x.bin", "scale": 2, "folder": "models/CUGAN/models-pro"},
24: {"param": "up2x-conservative.param", "bin": "up2x-conservative.bin", "scale": 2, "folder": "models/CUGAN/models-pro"},
25: {"param": "up2x-no-denoise.param", "bin": "up2x-no-denoise.bin", "scale": 2, "folder": "models/CUGAN/models-pro"},

26: {"param": "up3x-denoise3x", "bin": "denoise3x-up3x", "scale": 3, "folder": "models/CUGAN/models-pro"},
27: {"param": "up3x-conservative", "bin": "up3x-conservative.bin", "scale": 3, "folder": "models/CUGAN/models-pro"},
28: {"param": "up3x-no-denoise.param", "bin": "up3x-no-denoise.bin", "scale": 3, "folder": "models/CUGAN/models-pro"},

#shufflecugan
29: {"param": "sudo_shuffle_cugan-x2.param", "bin": "sudo_shuffle_cugan-x2.bin", "scale": 2, "folder": "models/SHUFFLECUGAN"},
```

Here, gpuid specifies the GPU device to use, tta_mode enables test-time augmentation, tilesize specifies the tile size
for processing (0 or >= 32), and model specifies the num of the pre-trained model to use.

Once the model is initialized, you can use the upscale method to super-resolve your images:

### Pillow

```python
from PIL import Image

upscale = upscale(gpuid=0)
with Image.open("input.jpg") as image:
    image = upscale.process_pil(image)
    image.save("output.jpg", quality=95)
```

### opencv-python

```python
import cv2

upscale = upscale(gpuid=0)
image = cv2.imdecode(np.fromfile("input.jpg", dtype=np.uint8), cv2.IMREAD_COLOR)
image = upscale.process_cv2(image)
cv2.imencode(".jpg", image)[1].tofile("output_cv2.jpg")
```

### ffmpeg

```python
import subprocess as sp

# your ffmpeg parameters
command_out = [FFMPEG_BIN, ........]
command_in = [FFMPEG_BIN, ........]
pipe_out = sp.Popen(command_out, stdout=sp.PIPE, bufsize=10 ** 8)
pipe_in = sp.Popen(command_in, stdin=sp.PIPE)
realesrgan = Realesrgan(gpuid=0)
while True:
    raw_image = pipe_out.stdout.read(src_width * src_height * 3)
    if not raw_image:
        break
    raw_image = realesrgan.process_bytes(raw_image, src_width, src_height, 3)
    pipe_in.stdin.write(raw_image)
```

# Build

[here](https://github.com/Tohrusky/realesrgan-ncnn-py/blob/main/.github/workflows/Release.yml)

_The project just only been tested in Ubuntu 18+ and Debian 9+ environments on Linux, so if the project does not work on
your system, please try building it._

# References

The following references were used in the development of this project:

[xinntao/Real-ESRGAN-ncnn-vulkan](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan) - This project was the main
inspiration for our work. It provided the core implementation of the Real-ESRGAN algorithm using the ncnn and Vulkan
libraries.

[Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) - Real-ESRGAN is an AI super resolution model, aims at developing
Practical Algorithms for General Image/Video Restoration.

[media2x/realsr-ncnn-vulkan-python](https://github.com/media2x/realsr-ncnn-vulkan-python) - This project was used as a
reference for implementing the wrapper. _Special thanks_ to the original author for sharing the code.

[ncnn](https://github.com/Tencent/ncnn) - ncnn is a high-performance neural network inference framework developed by
Tencent AI Lab.

# License

This project is licensed under the BSD 3-Clause - see
the [LICENSE file](https://github.com/Tohrusky/realesrgan-ncnn-py/blob/main/LICENSE) for details.
