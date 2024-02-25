#ifndef UPSCALE_NCNN_VULKAN_UPSCALE_WRAPPED_H
#define UPSCALE_NCNN_VULKAN_UPSCALE_WRAPPED_H

#include "upscale.h"
#include "pybind11/include/pybind11/pybind11.h"
#include <locale>
#include <codecvt>
#include <utility>

// wrapper class of ncnn::Mat
class UPSCALEImage {
public:
    std::string d;
    int w;
    int h;
    int c;

    UPSCALEImage(std::string d, int w, int h, int c);

    void set_data(std::string data);

    pybind11::bytes get_data() const;
};

class UPSCALEWrapped : public UPSCALE {
public:
    UPSCALEWrapped(int gpuid, bool tta_mode);

    int get_tilesize() const;

    // upscale parameters
    void set_parameters(int _tilesize, int _scale);

    int load(const std::string &parampath, const std::string &modelpath);

    int process(const UPSCALEImage &inimage, UPSCALEImage &outimage) const;

private:
    int gpuid;
};

int get_gpu_count();

void destroy_gpu_instance();

#endif // UPSCALE_NCNN_VULKAN_UPSCALE_WRAPPED_H