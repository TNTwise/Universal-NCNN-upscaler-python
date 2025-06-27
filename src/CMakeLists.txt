project(upscale-ncnn-vulkan-python)

cmake_minimum_required(VERSION 3.9)
cmake_policy(SET CMP0078 NEW)
cmake_policy(SET CMP0086 NEW)
cmake_policy(SET CMP0091 NEW)
set(CMAKE_POLICY_DEFAULT_CMP0091 NEW)
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE release CACHE STRING "Choose the type of build" FORCE)
endif()



option(USE_SYSTEM_NCNN "build with system libncnn" OFF)
option(USE_SYSTEM_WEBP "build with system libwebp" OFF)
option(USE_STATIC_MOLTENVK "link moltenvk static library" OFF)

find_package(Threads)
find_package(OpenMP)
find_package(Vulkan REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
target_include_directories(your_target PRIVATE ${Python3_INCLUDE_DIRS})
target_link_libraries(your_target PRIVATE ${Python3_LIBRARIES})

find_program(GLSLANGVALIDATOR_EXECUTABLE NAMES glslangValidator PATHS $ENV{VULKAN_SDK}/bin NO_CMAKE_FIND_ROOT_PATH)
message(STATUS "Found glslangValidator: ${GLSLANGVALIDATOR_EXECUTABLE}")

macro(upscale_add_shader SHADER_SRC)
    set(SHADER_SRC_FULLPATH ${CMAKE_CURRENT_SOURCE_DIR}/upscale-ncnn-vulkan/src/${SHADER_SRC})

    get_filename_component(SHADER_SRC_NAME_WE ${CMAKE_CURRENT_SOURCE_DIR}/realsr-ncnn-vulkan/src/${SHADER_SRC} NAME_WE)
    set(SHADER_SPV_HEX_FILE ${CMAKE_CURRENT_BINARY_DIR}/${SHADER_SRC_NAME_WE}.spv.hex.h)
    add_custom_command(
        OUTPUT ${SHADER_SPV_HEX_FILE}
        COMMAND ${GLSLANGVALIDATOR_EXECUTABLE}
        ARGS -V -s -x -o ${SHADER_SPV_HEX_FILE} ${SHADER_SRC_FULLPATH}
        DEPENDS ${SHADER_SRC_FULLPATH}
        COMMENT "Building SPIR-V module ${SHADER_SRC_NAME_WE}.spv"
        VERBATIM
    )
    set_source_files_properties(${SHADER_SPV_HEX_FILE} PROPERTIES GENERATED TRUE)
    list(APPEND SHADER_SPV_HEX_FILES ${SHADER_SPV_HEX_FILE})

    # fp16 storage
    set(SHADER_fp16s_SRC_NAME_WE "${SHADER_SRC_NAME_WE}_fp16s")

    set(SHADER_fp16s_SPV_HEX_FILE ${CMAKE_CURRENT_BINARY_DIR}/${SHADER_fp16s_SRC_NAME_WE}.spv.hex.h)
    add_custom_command(
        OUTPUT ${SHADER_fp16s_SPV_HEX_FILE}
        COMMAND ${GLSLANGVALIDATOR_EXECUTABLE}
        ARGS -DNCNN_fp16_storage=1 -V -s -x -o ${SHADER_fp16s_SPV_HEX_FILE} ${SHADER_SRC_FULLPATH}
        DEPENDS ${SHADER_SRC_FULLPATH}
        COMMENT "Building SPIR-V module ${SHADER_fp16s_SRC_NAME_WE}.spv"
        VERBATIM
    )
    set_source_files_properties(${SHADER_fp16s_SPV_HEX_FILE} PROPERTIES GENERATED TRUE)
    list(APPEND SHADER_SPV_HEX_FILES ${SHADER_fp16s_SPV_HEX_FILE})

    # int8 storage
    set(SHADER_int8s_SRC_NAME_WE "${SHADER_SRC_NAME_WE}_int8s")

    set(SHADER_int8s_SPV_HEX_FILE ${CMAKE_CURRENT_BINARY_DIR}/${SHADER_int8s_SRC_NAME_WE}.spv.hex.h)
    add_custom_command(
        OUTPUT ${SHADER_int8s_SPV_HEX_FILE}
        COMMAND ${GLSLANGVALIDATOR_EXECUTABLE}
        ARGS -DNCNN_fp16_storage=1 -DNCNN_int8_storage=1 -V -s -x -o ${SHADER_int8s_SPV_HEX_FILE} ${SHADER_SRC_FULLPATH}
        DEPENDS ${SHADER_SRC_FULLPATH}
        COMMENT "Building SPIR-V module ${SHADER_int8s_SRC_NAME_WE}.spv"
        VERBATIM
    )
    set_source_files_properties(${SHADER_int8s_SPV_HEX_FILE} PROPERTIES GENERATED TRUE)
    list(APPEND SHADER_SPV_HEX_FILES ${SHADER_int8s_SPV_HEX_FILE})
endmacro()

include_directories(${CMAKE_CURRENT_BINARY_DIR})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/upscale-ncnn-vulkan/src)
include_directories(.)

if(OPENMP_FOUND)
  message(STATUS "use openmp")
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
  set(CMAKE_EXE_LINKER_FLAGS
      "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
else()
  message(STATUS "not use openmp")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fexceptions -frtti")
endif()

# enable global link time optimization
cmake_policy(SET CMP0069 NEW)
set(CMAKE_POLICY_DEFAULT_CMP0069 NEW)
include(CheckIPOSupported)
check_ipo_supported(RESULT ipo_supported OUTPUT ipo_supported_output)
if(ipo_supported)
  set(CMAKE_INTERPROCEDURAL_OPTIMIZATION TRUE)
else()
  message(WARNING "IPO is not supported: ${ipo_supported_output}")
endif()

if(USE_SYSTEM_NCNN)
    set(GLSLANG_TARGET_DIR "GLSLANG-NOTFOUND" CACHE PATH "Absolute path to glslangTargets.cmake directory")
    if(NOT GLSLANG_TARGET_DIR AND NOT DEFINED ENV{GLSLANG_TARGET_DIR})
        message(WARNING "GLSLANG_TARGET_DIR must be defined! USE_SYSTEM_NCNN will be turned off.")
        set(USE_SYSTEM_NCNN OFF)
    else()
        message(STATUS "Using glslang install located at ${GLSLANG_TARGET_DIR}")

        find_package(Threads)

        include("${GLSLANG_TARGET_DIR}/OSDependentTargets.cmake")
        include("${GLSLANG_TARGET_DIR}/OGLCompilerTargets.cmake")
        if(EXISTS "${GLSLANG_TARGET_DIR}/HLSLTargets.cmake")
            # hlsl support can be optional
            include("${GLSLANG_TARGET_DIR}/HLSLTargets.cmake")
        endif()
        include("${GLSLANG_TARGET_DIR}/glslangTargets.cmake")
        include("${GLSLANG_TARGET_DIR}/SPIRVTargets.cmake")

    if(NOT TARGET glslang OR NOT TARGET SPIRV)
      message(
        WARNING
          "glslang or SPIRV target not found! USE_SYSTEM_NCNN will be turned off."
      )
      set(USE_SYSTEM_NCNN OFF)
    endif()
  endif()
endif()

if(USE_SYSTEM_NCNN)
  find_package(ncnn)
  if(NOT TARGET ncnn)
    message(
      WARNING "ncnn target not found! USE_SYSTEM_NCNN will be turned off.")
    set(USE_SYSTEM_NCNN OFF)
  endif()
endif()

if(NOT USE_SYSTEM_NCNN)
  # build ncnn library
  if(NOT EXISTS
     "${CMAKE_CURRENT_SOURCE_DIR}/upscale-ncnn-vulkan/src/ncnn/CMakeLists.txt")
    message(
      FATAL_ERROR
        "The submodules were not downloaded! Please update submodules with \"git submodule update --init --recursive\" and try again."
    )
  endif()

  option(NCNN_INSTALL_SDK "" OFF)
  option(NCNN_PIXEL_ROTATE "" OFF)
  option(NCNN_VULKAN "" ON)
  option(NCNN_VULKAN_ONLINE_SPIRV "" ON)
  option(NCNN_BUILD_BENCHMARK "" OFF)
  option(NCNN_BUILD_TESTS "" OFF)
  option(NCNN_BUILD_TOOLS "" OFF)
  option(NCNN_BUILD_EXAMPLES "" OFF)
  option(NCNN_DISABLE_RTTI "" OFF)
  option(NCNN_DISABLE_EXCEPTION "" OFF)
  option(NCNN_SIMPLEVK "" ON)
  

  
  option(WITH_LAYER_absval "" ON)
    option(WITH_LAYER_argmax "" ON)
    option(WITH_LAYER_batchnorm "" ON)
    option(WITH_LAYER_bias "" ON)
    option(WITH_LAYER_bnll "" ON)
    option(WITH_LAYER_concat "" ON)
    option(WITH_LAYER_convolution "" ON)
    option(WITH_LAYER_crop "" ON)
    option(WITH_LAYER_deconvolution "" ON)
    option(WITH_LAYER_dropout "" ON)
    option(WITH_LAYER_eltwise "" ON)
    option(WITH_LAYER_elu "" ON)
    option(WITH_LAYER_embed "" ON)
    option(WITH_LAYER_exp "" ON)
    option(WITH_LAYER_flatten "" ON)
    option(WITH_LAYER_innerproduct "" ON)
    option(WITH_LAYER_input "" ON)
    option(WITH_LAYER_log "" ON)
    option(WITH_LAYER_lrn "" ON)
    option(WITH_LAYER_memorydata "" ON)
    option(WITH_LAYER_mvn "" ON)
    option(WITH_LAYER_pooling "" ON)
    option(WITH_LAYER_power "" ON)
    option(WITH_LAYER_prelu "" ON)
    option(WITH_LAYER_proposal "" ON)
    option(WITH_LAYER_reduction "" ON)
    option(WITH_LAYER_relu "" ON)
    option(WITH_LAYER_reshape "" ON)
    option(WITH_LAYER_roipooling "" ON)
    option(WITH_LAYER_scale "" ON)
    option(WITH_LAYER_sigmoid "" ON)
    option(WITH_LAYER_slice "" ON)
    option(WITH_LAYER_softmax "" ON)
    option(WITH_LAYER_split "" ON)
    option(WITH_LAYER_spp "" ON)
    option(WITH_LAYER_tanh "" ON)
    option(WITH_LAYER_threshold "" ON)
    option(WITH_LAYER_tile "" ON)
    option(WITH_LAYER_rnn "" ON)
    option(WITH_LAYER_lstm "" ON)
    option(WITH_LAYER_binaryop "" ON)
    option(WITH_LAYER_unaryop "" ON)
    option(WITH_LAYER_convolutiondepthwise "" ON)
    option(WITH_LAYER_padding "" ON)
    option(WITH_LAYER_squeeze "" ON)
    option(WITH_LAYER_expanddims "" ON)
    option(WITH_LAYER_normalize "" ON)
    option(WITH_LAYER_permute "" ON)
    option(WITH_LAYER_priorbox "" ON)
    option(WITH_LAYER_detectionoutput "" ON)
    option(WITH_LAYER_interp "" ON)
    option(WITH_LAYER_deconvolutiondepthwise "" ON)
    option(WITH_LAYER_shufflechannel "" ON)
    option(WITH_LAYER_instancenorm "" ON)
    option(WITH_LAYER_clip "" ON)
    option(WITH_LAYER_reorg "" ON)
    option(WITH_LAYER_yolodetectionoutput "" ON)
    option(WITH_LAYER_quantize "" ON)
    option(WITH_LAYER_dequantize "" ON)
    option(WITH_LAYER_yolov3detectionoutput "" ON)
    option(WITH_LAYER_psroipooling "" ON)
    option(WITH_LAYER_roialign "" ON)
    option(WITH_LAYER_packing "" ON)
    option(WITH_LAYER_requantize "" ON)
    option(WITH_LAYER_cast "" ON)
    option(WITH_LAYER_hardsigmoid "" ON)
    option(WITH_LAYER_selu "" ON)
    option(WITH_LAYER_hardswish "" ON)
    option(WITH_LAYER_noop "" ON)
    option(WITH_LAYER_pixelshuffle "" ON)
    option(WITH_LAYER_deepcopy "" ON)
    option(WITH_LAYER_mish "" ON)
    option(WITH_LAYER_statisticspooling "" ON)
    option(WITH_LAYER_swish "" ON)
    option(WITH_LAYER_gemm "" ON)
    option(WITH_LAYER_groupnorm "" ON)
    option(WITH_LAYER_layernorm "" ON)
    option(WITH_LAYER_softplus "" ON)
    option(WITH_LAYER_gru "" ON)
    option(WITH_LAYER_multiheadattention "" ON)
    option(WITH_LAYER_gelu "" ON)
    option(WITH_LAYER_convolution1d "" ON)
    option(WITH_LAYER_pooling1d "" ON)
    option(WITH_LAYER_convolutiondepthwise1d "" ON)
    option(WITH_LAYER_convolution3d "" ON)
    option(WITH_LAYER_convolutiondepthwise3d "" ON)
    option(WITH_LAYER_pooling3d "" ON)
    option(WITH_LAYER_matmul "" ON)
    option(WITH_LAYER_deconvolution1d "" ON)
    option(WITH_LAYER_deconvolutiondepthwise1d "" ON)
    option(WITH_LAYER_deconvolution3d "" ON)
    option(WITH_LAYER_deconvolutiondepthwise3d "" ON)
    option(WITH_LAYER_einsum "" ON)
    option(WITH_LAYER_deformableconv2d "" ON)
    option(WITH_LAYER_glu "" ON)
    option(WITH_LAYER_fold "" ON)
    option(WITH_LAYER_unfold "" ON)
    option(WITH_LAYER_gridsample "" ON)
    option(WITH_LAYER_cumulativesum "" ON)
    option(WITH_LAYER_copyto "" ON)
    option(WITH_LAYER_erf "" ON)
    option(WITH_LAYER_diag "" ON)
    option(WITH_LAYER_celu "" ON)
    option(WITH_LAYER_shrink "" ON)

  add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/upscale-ncnn-vulkan/src/ncnn)
endif()

set(SHADER_SPV_HEX_FILES)

upscale_add_shader(upscale_preproc.comp)
upscale_add_shader(upscale_postproc.comp)
upscale_add_shader(upscale_preproc_tta.comp)
upscale_add_shader(upscale_postproc_tta.comp)

add_custom_target(generate-spirv DEPENDS ${SHADER_SPV_HEX_FILES})

add_subdirectory(pybind11)

pybind11_add_module(upscale_ncnn_vulkan_wrapper  upscale_wrapped.cpp upscale_wrapped.h upscale-ncnn-vulkan/src/upscale.h upscale-ncnn-vulkan/src/upscale.cpp)

add_dependencies(upscale_ncnn_vulkan_wrapper generate-spirv)

set_property(TARGET upscale_ncnn_vulkan_wrapper PROPERTY CXX_STANDARD 11)

set(UPSCALE_LINK_LIBRARIES ncnn ${Vulkan_LIBRARY})

if(USE_STATIC_MOLTENVK)
  find_library(CoreFoundation NAMES CoreFoundation)
  find_library(Foundation NAMES Foundation)
  find_library(Metal NAMES Metal)
  find_library(QuartzCore NAMES QuartzCore)
  find_library(CoreGraphics NAMES CoreGraphics)
  find_library(Cocoa NAMES Cocoa)
  find_library(IOKit NAMES IOKit)
  find_library(IOSurface NAMES IOSurface)

  list(
    APPEND
    UPSCALE_LINK_LIBRARIES
    ${Metal}
    ${QuartzCore}
    ${CoreGraphics}
    ${Cocoa}
    ${IOKit}
    ${IOSurface}
    ${Foundation}
    ${CoreFoundation})
endif()

if(OPENMP_FOUND)
  list(APPEND UPSCALE_LINK_LIBRARIES ${OpenMP_CXX_LIBRARIES})
endif()

target_link_libraries(upscale_ncnn_vulkan_wrapper PRIVATE ${UPSCALE_LINK_LIBRARIES})
