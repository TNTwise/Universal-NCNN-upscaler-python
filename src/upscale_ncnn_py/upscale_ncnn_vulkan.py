import pathlib
from typing import Dict, Optional, Union

import cv2
try:
    import torch
except:
    pass

import numpy as np
from PIL import Image
from sympy import Q

try:
    from . import upscale_ncnn_vulkan_wrapper as wrapped
except:
    import upscale_ncnn_vulkan_wrapper as wrapped


class UPSCALE:
    def __init__(self, gpuid: int = 0, tta_mode: bool = False, tilesize: int = 0, model: int = 0 ,num_threads: int = 1, model_str: str = "", scale: int = 0):
        assert gpuid >= -1, "gpuid must >= -1"
        assert tilesize == 0 or tilesize >= 32, "tilesize must >= 32 or be 0"
        assert model >= -1, "model must > 0 or -1"
        assert num_threads >= 1, "num_threads must be a positive integer"
        self._gpuid = gpuid
        self._model_str = model_str
        self._upscale_object = wrapped.UPSCALEWrapped(gpuid, tta_mode, num_threads)

        self._tilesize = tilesize
        self._model = model
        self._scale = scale

        if self._model > -1:
            self._load(scale=scale)

        self.raw_in_image = None
        self.raw_out_image = None

        self.channels = None
        self.out_bytes = None
        
        
    def _set_parameters(self) -> None:
        self._upscale_object.set_parameters(self._tilesize, self._scale)

    def _load(
        self, param_path: Optional[pathlib.Path] = None, model_path: Optional[pathlib.Path] = None, scale: int = 0
    ) -> None:
        model_dict: Dict[int, Dict[str, Union[str, int]]] = {
      
        #span
        0: {"param": "spanx2_ch48.param", "bin": "spanx2_ch48.bin", "scale": 2, "folder": "models/SPAN"},
        1: {"param": "spanx2_ch52.param", "bin": "spanx2_ch52.bin", "scale": 2, "folder": "models/SPAN"},
        2: {"param": "spanx4_ch48.param", "bin": "spanx4_ch48.bin", "scale": 4, "folder": "models/SPAN"},
        3: {"param": "spanx4_ch52.param", "bin": "spanx4_ch52.bin", "scale": 4, "folder": "models/SPAN"},
        #custom span
        4: {"param": "2x_ModernSpanimationV1.param", "bin": "2x_ModernSpanimationV1.bin", "scale": 2, "folder": "models/SPAN"},
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
        }

        if self._model == -1:
            if param_path is None and model_path is None and scale == 0:
                raise ValueError("param_path, model_path and scale must be specified when model == -1")
            if param_path is None or model_path is None:
                raise ValueError("param_path and model_path must be specified when model == -1")
            if scale == 0:
                raise ValueError("scale must be specified when model == -1")
        else:
            if self._model_str == "":
                model_dir = pathlib.Path(__file__).parent / model_dict[self._model].get("folder", "models")

                param_path = model_dir / pathlib.Path(str(model_dict[self._model]["param"]))
                model_path = model_dir / pathlib.Path(str(model_dict[self._model]["bin"]))
            else:
                model_dir = pathlib.Path(self._model_str).parent
                
                param_path = model_dir / pathlib.Path(str(self._model_str.split("/")[-1]+".param"))
                model_path = model_dir / pathlib.Path(str(self._model_str.split("/")[-1]+".bin"))
                
                # print (model_dir,param_path,model_path)
        self._scale = scale if scale != 0 else int(model_dict[self._model]["scale"])
        self._set_parameters()

        if param_path is None or model_path is None:
            raise ValueError("param_path and model_path is None")

        self._upscale_object.load(str(param_path), str(model_path))

    def process(self) -> None:
        self._upscale_object.process(self.raw_in_image, self.raw_out_image)

    def process_pil(self, _image: Image) -> Image:
        in_bytes = _image.tobytes()
        channels = int(len(in_bytes) / (_image.width * _image.height))
        out_bytes = (self._scale**2) * len(in_bytes) * b"\x00"

        self.raw_in_image = wrapped.UPSCALEImage(in_bytes, _image.width, _image.height, channels)

        self.raw_out_image = wrapped.UPSCALEImage(
            out_bytes,
            self._scale * _image.width,
            self._scale * _image.height,
            channels,
        )

        self.process()

        return Image.frombytes(
            _image.mode,
            (
                self._scale * _image.width,
                self._scale * _image.height,
            ),
            self.raw_out_image.get_data(),
        )

    def process_cv2(self, _image: np.ndarray) -> np.ndarray:

        in_bytes = _image.tobytes()
        if self.channels == None:
            self.channels = int(len(in_bytes) / (_image.shape[1] * _image.shape[0]))
            self.out_bytes = (self._scale**2) * len(in_bytes) * b"\x00"

        self.raw_in_image = wrapped.UPSCALEImage(in_bytes, _image.shape[1], _image.shape[0], self.channels)

        self.raw_out_image = wrapped.UPSCALEImage(
            self.out_bytes,
            self._scale * _image.shape[1],
            self._scale * _image.shape[0],
            self.channels,
        )

        self.process()

        

        return np.frombuffer(self.raw_out_image.get_data(), dtype=np.uint8).reshape(
            self._scale * _image.shape[0], self._scale * _image.shape[1], self.channels
        )

    def process_bytes(self, _image_bytes: bytes, width: int, height: int, channels: int) -> bytes:
        if self.raw_in_image is None and self.raw_out_image is None:
            self.raw_in_image = wrapped.UPSCALEImage(_image_bytes, width, height, channels)

            self.raw_out_image = wrapped.UPSCALEImage(
                (self._scale**2) * len(_image_bytes) * b"\x00",
                self._scale * width,
                self._scale * height,
                channels,
            )

        self.raw_in_image.set_data(_image_bytes)

        self.process()

        return self.raw_out_image.get_data()
    
    def process_torch(self, image):
        # MAYBE IT WORKS
        in_bytes = image.numpy().tobytes()
        if self.channels == None:
            self.channels = int(len(in_bytes) / (image.shape[1] * image.shape[0]))
            self.out_bytes = (self._scale**2) * len(in_bytes) * b"\x00"
        
        self.raw_in_image = wrapped.UPSCALEImage(in_bytes, image.shape[1], image.shape[0], self.channels)

        self.raw_out_image = wrapped.UPSCALEImage(
            self.out_bytes,
            self._scale * image.shape[1],
            self._scale * image.shape[0],
            self.channels,
        )

        return torch.frombuffer(self.process_bytes(in_bytes, image.shape[1], image.shape[0], self.channels), dtype=torch.uint8).reshape(
            self._scale * image.shape[0], self._scale * image.shape[1], self.channels
        )
    
