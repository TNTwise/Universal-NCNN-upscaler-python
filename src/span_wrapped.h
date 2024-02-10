#ifndef SPAN_NCNN_VULKAN_SPAN_WRAPPED_H
#define SPAN_NCNN_VULKAN_SPAN_WRAPPED_H

#include "span.h"
#include "pybind11/include/pybind11/pybind11.h"
#include <locale>
#include <codecvt>
#include <utility>

// wrapper class of ncnn::Mat
class SpanImage {
public:
    std::string d;
    int w;
    int h;
    int c;

    SpanImage(std::string d, int w, int h, int c);

    void set_data(std::string data);

    pybind11::bytes get_data() const;
};

class SpanWrapped : public Span {
public:
    SpanWrapped(int gpuid, bool tta_mode);

    int get_tilesize() const;

    // span parameters
    void set_parameters(int _tilesize, int _scale);

    int load(const std::string &parampath, const std::string &modelpath);

    int process(const SpanImage &inimage, SpanImage &outimage) const;

private:
    int gpuid;
};

int get_gpu_count();

void destroy_gpu_instance();

#endif // SPAN_NCNN_VULKAN_SPAN_WRAPPED_H