#include "span_wrapped.h"

// Image Data Structure
SpanImage::SpanImage(std::string d, int w, int h, int c) {
    this->d = std::move(d);
    this->w = w;
    this->h = h;
    this->c = c;
}

void SpanImage::set_data(std::string data) {
    this->d = std::move(data);
}

pybind11::bytes SpanImage::get_data() const {
    return pybind11::bytes(this->d);
}

// SpanWrapped
SpanWrapped::SpanWrapped(int gpuid, bool tta_mode): Span(gpuid, tta_mode) {
    this->gpuid = gpuid;
}

int SpanWrapped::get_tilesize() const {
    int tilesize = 0;

    if (this->gpuid < 0) {
        return 400;
    }

    uint32_t heap_budget = ncnn::get_gpu_device(this->gpuid)->get_heap_budget();

    if (heap_budget >= 1900) {
        tilesize = 200;
    } else if (heap_budget >= 550) {
        tilesize = 100;
    } else if (heap_budget >= 190) {
        tilesize = 64;
    } else {
        tilesize = 32;
    }

    return tilesize;
}

void SpanWrapped::set_parameters(int _tilesize, int _scale) {
    Span::tilesize = _tilesize ? _tilesize : SpanWrapped::get_tilesize();
    Span::scale = _scale;
    Span::prepadding = 10;
}

int SpanWrapped::load(const std::string &parampath, const std::string &modelpath) {
#if _WIN32
    // convert string to wstring
    auto to_wide_string = [&](const std::string& input) {
        std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;
        return converter.from_bytes(input);
    };
    return Span::load(to_wide_string(parampath), to_wide_string(modelpath));
#else
    return Span::load(parampath, modelpath);
#endif
}

int SpanWrapped::process(const SpanImage &inimage, SpanImage &outimage) const {
    int c = inimage.c;
    ncnn::Mat inimagemat =
            ncnn::Mat(inimage.w, inimage.h, (void *) inimage.d.data(), (size_t) c, c);
    ncnn::Mat outimagemat =
            ncnn::Mat(outimage.w, outimage.h, (void *) outimage.d.data(), (size_t) c, c);
    return Span::process(inimagemat, outimagemat);
}

int get_gpu_count() { return ncnn::get_gpu_count(); }

void destroy_gpu_instance() { ncnn::destroy_gpu_instance(); }

PYBIND11_MODULE(span_ncnn_vulkan_wrapper, m) {
    pybind11::class_<SpanWrapped>(m, "SpanWrapped")
            .def(pybind11::init<int, bool>())
            .def("load", &SpanWrapped::load)
            .def("process", &SpanWrapped::process)
            .def("set_parameters", &SpanWrapped::set_parameters);

    pybind11::class_<SpanImage>(m, "SpanImage")
            .def(pybind11::init<std::string, int, int, int>())
            .def("get_data", &SpanImage::get_data)
            .def("set_data", &SpanImage::set_data);

    m.def("get_gpu_count", &get_gpu_count);

    m.def("destroy_gpu_instance", &destroy_gpu_instance);
}