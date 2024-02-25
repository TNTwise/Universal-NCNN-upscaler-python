import pathlib
from typing import Dict, Optional, Union

import cv2
import numpy as np
from PIL import Image

try:
    from . import upscale_ncnn_vulkan_wrapper as wrapped
except ImportError:
    import upscale_ncnn_vulkan_wrapper as wrapped


class UPSCALE:
    def __init__(self, gpuid: int = 0, tta_mode: bool = False, tilesize: int = 0, model: int = 0):
        assert gpuid >= -1, "gpuid must >= -1"
        assert tilesize == 0 or tilesize >= 32, "tilesize must >= 32 or be 0"
        assert model >= -1, "model must > 0 or -1"

        self._gpuid = gpuid

        self._upscale_object = wrapped.UPSCALEWrapped(gpuid, tta_mode)

        self._tilesize = tilesize
        self._model = model
        self._scale = 2

        if self._model > -1:
            self._load()

        self.raw_in_image = None
        self.raw_out_image = None

    def _set_parameters(self) -> None:
        self._upscale_object.set_parameters(self._tilesize, self._scale)

    def _load(
        self, param_path: Optional[pathlib.Path] = None, model_path: Optional[pathlib.Path] = None, scale: int = 0
    ) -> None:
        model_dict: Dict[int, Dict[str, Union[str, int]]] = {
            0: {"param": "upscalex2_ch48.param", "bin": "upscalex2_ch48.bin", "scale": 2, "folder": "models/SPAN"},
            1: {"param": "upscalex2_ch52.param", "bin": "upscalex2_ch52.bin", "scale": 2, "folder": "models/SPAN"},
            2: {"param": "upscalex4_ch48.param", "bin": "upscalex4_ch48.bin", "scale": 4, "folder": "models/SPAN"},
            3: {"param": "upscalex4_ch52.param", "bin": "upscalex4_ch52.bin", "scale": 4, "folder": "models/SPAN"},
            
            4: {"param": "realesr-animevideov3-x2.param", "bin": "realesr-animevideov3-x2.bin", "scale": 2, "folder": "models/ESRGAN"},
            5: {"param": "realesr-animevideov3-x3.param", "bin": "realesr-animevideov3-x3.bin", "scale": 3, "folder": "models/ESRGAN"},
            6: {"param": "realesr-animevideov3-x4.param", "bin": "realesr-animevideov3-x4.bin", "scale": 4, "folder": "models/ESRGAN"},
            7: {"param": "realesrgan-x4plus-x4.param", "bin": "realesrgan-x4plus.bin", "scale": 4, "folder": "models/ESRGAN"},
            8: {"param": "realesrgan-x4plus-anime.param", "bin": "realesrgan-x4plus-anime.bin", "scale": 4, "folder": "models/ESRGAN"},
            
            9: {"param": "up2x-conservative.param", "bin": "up2x-conservative.bin", "scale": 2, "folder": "models/CUGAN/models-se"},
            10: {"param": "up2x-no-denoise.param", "bin": "up2x-no-denoise.bin", "scale": 2, "folder": "models/CUGAN/models-se"},

            11: {"param": "up4x-conservative.param", "bin": "up4x-conservative.bin", "scale": 4, "folder": "models/CUGAN/models-se"},
            12: {"param": "up4x-no-denoise.param", "bin": "up4x-no-denoise.bin", "scale": 4, "folder": "models/CUGAN/models-se"},
            
            13: {"param": "up2x-conservative.param", "bin": "up2x-conservative.bin", "scale": 2, "folder": "models/CUGAN/models-pro"},
            14: {"param": "up2x-no-denoise.param", "bin": "up2x-no-denoise.bin", "scale": 2, "folder": "models/CUGAN/models-pro"},
            
            15: {"param": "sudo_shuffle_cugan-x2.param", "bin": "sudo_shuffle_cugan-x2.bin", "scale": 2, "folder": "models/SHUFFLECUGAN"},
        }

        if self._model == -1:
            if param_path is None and model_path is None and scale == 0:
                raise ValueError("param_path, model_path and scale must be specified when model == -1")
            if param_path is None or model_path is None:
                raise ValueError("param_path and model_path must be specified when model == -1")
            if scale == 0:
                raise ValueError("scale must be specified when model == -1")
        else:
            model_dir = pathlib.Path(__file__).parent / model_dict[self._model].get("folder", "models")

            param_path = model_dir / pathlib.Path(str(model_dict[self._model]["param"]))
            model_path = model_dir / pathlib.Path(str(model_dict[self._model]["bin"]))

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

        self.raw_in_image = wrapped.SpanImage(in_bytes, _image.width, _image.height, channels)

        self.raw_out_image = wrapped.SpanImage(
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
        _image = cv2.cvtColor(_image, cv2.COLOR_BGR2RGB)

        in_bytes = _image.tobytes()
        channels = int(len(in_bytes) / (_image.shape[1] * _image.shape[0]))
        out_bytes = (self._scale**2) * len(in_bytes) * b"\x00"

        self.raw_in_image = wrapped.UPSCALEImage(in_bytes, _image.shape[1], _image.shape[0], channels)

        self.raw_out_image = wrapped.UPSCALEImage(
            out_bytes,
            self._scale * _image.shape[1],
            self._scale * _image.shape[0],
            channels,
        )

        self.process()

        res = np.frombuffer(self.raw_out_image.get_data(), dtype=np.uint8).reshape(
            self._scale * _image.shape[0], self._scale * _image.shape[1], channels
        )

        return cv2.cvtColor(res, cv2.COLOR_RGB2BGR)

    def process_bytes(self, _image_bytes: bytes, width: int, height: int, channels: int) -> bytes:
        if self.raw_in_image is None and self.raw_out_image is None:
            self.raw_in_image = wrapped.SpanImage(_image_bytes, width, height, channels)

            self.raw_out_image = wrapped.SpanImage(
                (self._scale**2) * len(_image_bytes) * b"\x00",
                self._scale * width,
                self._scale * height,
                channels,
            )

        self.raw_in_image.set_data(_image_bytes)

        self.process()

        return self.raw_out_image.get_data()
