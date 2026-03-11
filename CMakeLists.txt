# ========================
# fasttouch Python Binding
# ========================
cmake_minimum_required(VERSION 3.16)
project(fasttouch_python LANGUAGES CXX)

# --- C++ 标准 ---
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# --- 查找依赖 ---
find_package(pybind11 REQUIRED CONFIG)
find_package(Threads REQUIRED)

set(EIGEN3_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/third_party/eigen)
include_directories(${EIGEN3_INCLUDE_DIR})

# --- 定位原生库 
set(LIB_STARTOUCH ${CMAKE_CURRENT_SOURCE_DIR}/src/fasttouch_python_sdk/libstartouch.so)

if(NOT EXISTS ${LIB_STARTOUCH})
    message(FATAL_ERROR "libstartouch.so not found at ${LIB_STARTOUCH}")
endif()

# --- 构建 Python 扩展模块  ---
pybind11_add_module(fasttouch_python_sdk src/fasttouch_python_sdk/pybind_0825testfast.cpp)

# --- 包含路径 ---
target_include_directories(fasttouch_python_sdk PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src/fasttouch_python_sdk
    ${EIGEN3_INCLUDE_DIR}
)

# --- 链接库 ---
target_link_libraries(fasttouch_python_sdk PRIVATE
    ${LIB_STARTOUCH}
    Threads::Threads
)

# --- 设置 RPATH ---
set_target_properties(fasttouch_python_sdk PROPERTIES
    INSTALL_RPATH "$ORIGIN"
    BUILD_RPATH "$ORIGIN"
    SKIP_RPATH FALSE
)

# --- 安装规则 ---
install(TARGETS fasttouch_python_sdk
    LIBRARY DESTINATION fasttouch_python_sdk
    RUNTIME DESTINATION fasttouch_python_sdk
)

# 安装原生库和 Python 文件
install(FILES ${LIB_STARTOUCH}
    ${CMAKE_CURRENT_SOURCE_DIR}/src/fasttouch_python_sdk/__init__.py
    ${CMAKE_CURRENT_SOURCE_DIR}/src/fasttouch_python_sdk/fasttouch.py
    ${CMAKE_CURRENT_SOURCE_DIR}/src/fasttouch_python_sdk/utils.py
    DESTINATION fasttouch_python_sdk
)

install(DIRECTORY 
    ${CMAKE_CURRENT_SOURCE_DIR}/src/fasttouch_python_sdk/param_csv_gripper/
    DESTINATION fasttouch_python_sdk/param_csv_gripper
    FILES_MATCHING
    PATTERN "*.csv"
)