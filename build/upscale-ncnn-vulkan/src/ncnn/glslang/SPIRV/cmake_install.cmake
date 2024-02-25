# Install script for directory: /home/pax/Universal-NCNN-upscaler-python/src/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "0")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/home/pax/Universal-NCNN-upscaler-python/build/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV/libSPIRV.a")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake" TYPE FILE FILES "/home/pax/Universal-NCNN-upscaler-python/build/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV/SPIRVTargets.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/glslang/SPIRV" TYPE FILE FILES
    "/home/pax/Universal-NCNN-upscaler-python/src/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV/bitutils.h"
    "/home/pax/Universal-NCNN-upscaler-python/src/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV/spirv.hpp"
    "/home/pax/Universal-NCNN-upscaler-python/src/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV/GLSL.std.450.h"
    "/home/pax/Universal-NCNN-upscaler-python/src/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV/GLSL.ext.EXT.h"
    "/home/pax/Universal-NCNN-upscaler-python/src/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV/GLSL.ext.KHR.h"
    "/home/pax/Universal-NCNN-upscaler-python/src/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV/GlslangToSpv.h"
    "/home/pax/Universal-NCNN-upscaler-python/src/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV/hex_float.h"
    "/home/pax/Universal-NCNN-upscaler-python/src/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV/Logger.h"
    "/home/pax/Universal-NCNN-upscaler-python/src/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV/SpvBuilder.h"
    "/home/pax/Universal-NCNN-upscaler-python/src/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV/spvIR.h"
    "/home/pax/Universal-NCNN-upscaler-python/src/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV/doc.h"
    "/home/pax/Universal-NCNN-upscaler-python/src/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV/SpvTools.h"
    "/home/pax/Universal-NCNN-upscaler-python/src/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV/disassemble.h"
    "/home/pax/Universal-NCNN-upscaler-python/src/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV/GLSL.ext.AMD.h"
    "/home/pax/Universal-NCNN-upscaler-python/src/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV/GLSL.ext.NV.h"
    "/home/pax/Universal-NCNN-upscaler-python/src/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV/GLSL.ext.ARM.h"
    "/home/pax/Universal-NCNN-upscaler-python/src/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV/NonSemanticDebugPrintf.h"
    "/home/pax/Universal-NCNN-upscaler-python/src/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV/NonSemanticShaderDebugInfo100.h"
    "/home/pax/Universal-NCNN-upscaler-python/src/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV/SPVRemapper.h"
    "/home/pax/Universal-NCNN-upscaler-python/src/upscale-ncnn-vulkan/src/ncnn/glslang/SPIRV/doc.h"
    )
endif()

