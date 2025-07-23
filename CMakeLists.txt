cmake_minimum_required(VERSION 3.25 FATAL_ERROR)

set(CMAKE_UTIL_FILE "" CACHE STRING "...")
set(USE_CONAN "1" CACHE BOOL "...")

message(STATUS "USE_CONAN: '${USE_CONAN}'")

if("${USE_CONAN}")
    if("windows" IN_LIST "PRESET_NAME_ELEMENTS")
        find_program(CONAN_COMMAND NAMES "conan.exe" PATHS ENV CONAN_PATH ENV PATH REQUIRED NO_CACHE NO_DEFAULT_PATH)
    else()
        find_program(CONAN_COMMAND NAMES "conan" PATHS ENV CONAN_PATH ENV PATH REQUIRED NO_CACHE NO_DEFAULT_PATH)
    endif()
endif()

if("${CMAKE_UTIL_FILE}" STREQUAL "")
    if("$ENV{CMAKE_UTIL_FILE}" STREQUAL "")
        if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/build/dependencies/direct_deploy/exqudens-cmake/cmake/util.cmake")
            if("${USE_CONAN}")
                #[[execute_process(
                    COMMAND "${CONAN_COMMAND}" "user" "$ENV{CONAN_LOGIN_USERNAME}" "-r" "artifactory" "-p"
                    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
                    ENCODING "UTF-8"
                    COMMAND_ERROR_IS_FATAL "ANY"
                )]]
                execute_process(
                    COMMAND "${CONAN_COMMAND}" "install" "--tool-requires=exqudens-cmake/0.0.1" "--deployer" "direct_deploy" "--deployer-folder" "${CMAKE_SOURCE_DIR}/build/dependencies"
                    COMMAND_ECHO "STDERR"
                    ENCODING "UTF-8"
                    COMMAND_ERROR_IS_FATAL "ANY"
                )
                set(CMAKE_UTIL_FILE "${CMAKE_CURRENT_SOURCE_DIR}/build/dependencies/direct_deploy/exqudens-cmake/cmake/util.cmake" CACHE STRING "..." FORCE)
            else()
                message(FATAL_ERROR "Unable to resolve CMAKE_UTIL_FILE: '${CMAKE_UTIL_FILE}'")
            endif()
        else()
            set(CMAKE_UTIL_FILE "${CMAKE_CURRENT_SOURCE_DIR}/build/dependencies/direct_deploy/exqudens-cmake/cmake/util.cmake" CACHE STRING "..." FORCE)
        endif()
    else()
        set(CMAKE_UTIL_FILE "$ENV{CMAKE_UTIL_FILE}" CACHE STRING "..." FORCE)
    endif()
endif()

message(STATUS "CMAKE_UTIL_FILE: '${CMAKE_UTIL_FILE}'")

include("${CMAKE_UTIL_FILE}")

string(REPLACE "." ";" PRESET_NAME_ELEMENTS "${PRESET_NAME}")
if("msvc-x64-x64" IN_LIST "PRESET_NAME_ELEMENTS")
    if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/build/msvc-x64-x64-toolchain.cmake")
        set_msvc_toolchain(TOOLCHAIN_CONTENT
            PROCESSOR "x86_64"
            OS "${CMAKE_HOST_SYSTEM_NAME}"
            VERSION "17"
            HOST "x64"
            TARGET "x64"
            OUTPUT_FILE "${CMAKE_CURRENT_SOURCE_DIR}/build/msvc-x64-x64-toolchain.cmake"
        )
    endif()
elseif("gcc" IN_LIST PRESET_NAME_ELEMENTS)
    if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/build/gcc-toolchain.cmake")
        find_file(COMPILER_FILE NAMES "gcc" PATHS ENV GCC_PATH ENV PATH REQUIRED NO_CACHE NO_DEFAULT_PATH)
        set_gnu_toolchain(TOOLCHAIN_CONTENT
            PROCESSOR "x86_64"
            OS "${CMAKE_HOST_SYSTEM_NAME}"
            PATH "${COMPILER_FILE}"
            OUTPUT_FILE "${CMAKE_CURRENT_SOURCE_DIR}/build/gcc-toolchain.cmake"
        )
    endif()
endif()

message(STATUS "CMAKE_TOOLCHAIN_FILE: '${CMAKE_TOOLCHAIN_FILE}'")

file(READ "${CMAKE_CURRENT_SOURCE_DIR}/name-version.txt" INFO)
string(REPLACE ":" ";" INFO_LIST "${INFO}")
list(GET INFO_LIST 0 RAW_NAME)
list(GET INFO_LIST 1 RAW_VERSION)
string(STRIP "${RAW_NAME}" NAME)
string(STRIP "${RAW_VERSION}" VERSION)
project("${NAME}" VERSION "${VERSION}" LANGUAGES "NONE")

message(STATUS "PROJECT_NAME: '${PROJECT_NAME}'")
message(STATUS "PROJECT_VERSION: '${PROJECT_VERSION}'")

string(REPLACE "_" "-" BASE_DIR "${PROJECT_NAME}")
string(REPLACE "-c-" "-" BASE_DIR "${BASE_DIR}")
string(REPLACE "-" "/" BASE_DIR "${BASE_DIR}")

message(STATUS "BASE_DIR: '${BASE_DIR}'")

string(REPLACE "/" "_" BASE_NAME "${BASE_DIR}")
string(TOUPPER "${BASE_NAME}" BASE_NAME)

message(STATUS "BASE_NAME: '${BASE_NAME}'")

if("$ENV{CLION_IDE}")
    cmake_path(CONVERT "$ENV{PATH}" TO_CMAKE_PATH_LIST TMP_CMAKE_ENV_PATH NORMALIZE)
    list(REMOVE_AT TMP_CMAKE_ENV_PATH 0)
    cmake_path(CONVERT "${TMP_CMAKE_ENV_PATH}" TO_NATIVE_PATH_LIST TMP_NATIVE_ENV_PATH NORMALIZE)
    set("ENV{PATH}" "${TMP_NATIVE_ENV_PATH}")
endif()

enable_language("C")

if("${CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT}")
    set(CMAKE_INSTALL_PREFIX "${PROJECT_BINARY_DIR}/cmake-install" CACHE PATH "..." FORCE)
endif()
set(CMAKE_VERBOSE_MAKEFILE "TRUE" CACHE BOOL "" FORCE)
set(CMAKE_EXPORT_COMPILE_COMMANDS "TRUE" CACHE BOOL "" FORCE)

cmake_path(RELATIVE_PATH "PROJECT_BINARY_DIR" BASE_DIRECTORY "${PROJECT_SOURCE_DIR}" OUTPUT_VARIABLE "PROJECT_BINARY_DIR_REL")
cmake_path(CONVERT "$ENV{PATH}" TO_CMAKE_PATH_LIST "ENV_PATH" NORMALIZE)
set(CMAKE_OBJECT_PATH_MAX 1000)
set(CMAKE_SHARED_LIBRARY_PREFIX "")
set(CMAKE_SHARED_MODULE_PREFIX "")
set(CMAKE_STATIC_LIBRARY_PREFIX "")
set(CMAKE_IMPORT_LIBRARY_PREFIX "")
set(CMAKE_STAGING_PREFIX "")
set(CMAKE_FIND_LIBRARY_PREFIXES "" "lib")
set(CMAKE_FIND_USE_CMAKE_ENVIRONMENT_PATH FALSE)
set(CMAKE_FIND_USE_CMAKE_SYSTEM_PATH FALSE)
set(CMAKE_FIND_USE_SYSTEM_ENVIRONMENT_PATH TRUE)
set(CMAKE_FIND_USE_SYSTEM_PACKAGE_REGISTRY FALSE)
set(CMAKE_FIND_USE_PACKAGE_REGISTRY FALSE)
set(CMAKE_FIND_USE_PACKAGE_ROOT_PATH FALSE)
set(CMAKE_FIND_USE_CMAKE_PATH TRUE)
set(CMAKE_FIND_PACKAGE_PREFER_CONFIG FALSE)
set(CMAKE_BUILD_RPATH "\$ORIGIN")
set(CMAKE_INSTALL_RPATH "\$ORIGIN")
set(CMAKE_SKIP_BUILD_RPATH TRUE)
set(CMAKE_BUILD_RPATH_USE_ORIGIN TRUE)
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH FALSE)
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS FALSE)
set(CMAKE_C_VISIBILITY_PRESET "hidden")
set(CMAKE_VISIBILITY_INLINES_HIDDEN TRUE)
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED TRUE)
set(CMAKE_C_EXTENSIONS FALSE)

set(PYTHON_ENV_DIR_REL "build/sphinx/env")
if("windows" IN_LIST "PRESET_NAME_ELEMENTS")
    find_program(PYTHON_COMMAND NAMES "py.exe" PATHS ENV PYTHON_PATH ENV PATH REQUIRED NO_CACHE NO_DEFAULT_PATH)
    set(PYTHON_ENV_COMMAND "${PROJECT_SOURCE_DIR}/${PYTHON_ENV_DIR_REL}/Scripts/python.exe")
    set(SPHINX_BUILD_COMMAND "${PROJECT_SOURCE_DIR}/${PYTHON_ENV_DIR_REL}/Scripts/sphinx-build.exe")
else()
    find_program(PYTHON_COMMAND NAMES "python" PATHS ENV PYTHON_PATH ENV PATH REQUIRED NO_CACHE NO_DEFAULT_PATH)
    set(PYTHON_ENV_COMMAND "${PROJECT_SOURCE_DIR}/${PYTHON_ENV_DIR_REL}/bin/python")
    set(SPHINX_BUILD_COMMAND "${PROJECT_SOURCE_DIR}/${PYTHON_ENV_DIR_REL}/bin/sphinx-build")
endif()

add_library("${PROJECT_NAME}"
    "src/main/c/exqudens/math.h"
    "src/main/c/exqudens/math.c"
    "src/main/c/exqudens/string.h"
    "src/main/c/exqudens/string.c"
)
target_include_directories("${PROJECT_NAME}" PUBLIC
    "$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/src/main/c>"
    "$<INSTALL_INTERFACE:include>"
)
set_target_properties("${PROJECT_NAME}" PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY                "${PROJECT_BINARY_DIR}/main/bin"
    RUNTIME_OUTPUT_DIRECTORY_RELEASE        "${PROJECT_BINARY_DIR}/main/bin"
    RUNTIME_OUTPUT_DIRECTORY_RELWITHDEBINFO "${PROJECT_BINARY_DIR}/main/bin"
    RUNTIME_OUTPUT_DIRECTORY_MINSIZEREL     "${PROJECT_BINARY_DIR}/main/bin"
    RUNTIME_OUTPUT_DIRECTORY_DEBUG          "${PROJECT_BINARY_DIR}/main/bin"

    ARCHIVE_OUTPUT_DIRECTORY                "${PROJECT_BINARY_DIR}/main/lib"
    ARCHIVE_OUTPUT_DIRECTORY_RELEASE        "${PROJECT_BINARY_DIR}/main/lib"
    ARCHIVE_OUTPUT_DIRECTORY_RELWITHDEBINFO "${PROJECT_BINARY_DIR}/main/lib"
    ARCHIVE_OUTPUT_DIRECTORY_MINSIZEREL     "${PROJECT_BINARY_DIR}/main/lib"
    ARCHIVE_OUTPUT_DIRECTORY_DEBUG          "${PROJECT_BINARY_DIR}/main/lib"

    LIBRARY_OUTPUT_DIRECTORY                "${PROJECT_BINARY_DIR}/main/lib"
    LIBRARY_OUTPUT_DIRECTORY_RELEASE        "${PROJECT_BINARY_DIR}/main/lib"
    LIBRARY_OUTPUT_DIRECTORY_RELWITHDEBINFO "${PROJECT_BINARY_DIR}/main/lib"
    LIBRARY_OUTPUT_DIRECTORY_MINSIZEREL     "${PROJECT_BINARY_DIR}/main/lib"
    LIBRARY_OUTPUT_DIRECTORY_DEBUG          "${PROJECT_BINARY_DIR}/main/lib"
)

add_custom_command(
    OUTPUT "${PROJECT_SOURCE_DIR}/build/doxygen/main/xml/index.xml"
    COMMAND "${CMAKE_COMMAND}" "-P" "${CMAKE_UTIL_FILE}" "--" "doxygen"
            SOURCE_BASE_DIR "${PROJECT_SOURCE_DIR}"
            SOURCE_DIR "src/main/c"
            OUTPUT_DIR "build/doxygen/main"
            DOXYFILE "doc/main-doxygenfile.txt"
            CLEAN "1"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    USES_TERMINAL
    VERBATIM
)

add_custom_command(
    OUTPUT "${PROJECT_SOURCE_DIR}/build/doxygen/main-no-group/xml/index.xml"
    COMMAND "${CMAKE_COMMAND}" "-P" "${CMAKE_UTIL_FILE}" "--" "doxygen"
            SOURCE_BASE_DIR "${PROJECT_SOURCE_DIR}"
            SOURCE_DIR "src/main/c"
            OUTPUT_DIR "build/doxygen/main-no-group"
            DOXYFILE "doc/main-no-group-doxygenfile.txt"
            CLEAN "1"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    USES_TERMINAL
    VERBATIM
)

add_custom_command(
    OUTPUT "${SPHINX_BUILD_COMMAND}"
    COMMAND "${PYTHON_COMMAND}" "-m" "venv" "${PYTHON_ENV_DIR_REL}"
    COMMAND "${PYTHON_ENV_COMMAND}" "-m" "pip" "install"
            "--trusted-host" "pypi.org"
            "--trusted-host" "pypi.python.org"
            "--trusted-host" "files.pythonhosted.org"
            "-r" "doc/requirements.txt"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    USES_TERMINAL
    VERBATIM
)

add_custom_target("doc-all"
    COMMAND "${CMAKE_COMMAND}" "-E" "rm" "-rf" "${PROJECT_SOURCE_DIR}/build/doc/all"
    COMMAND "${SPHINX_BUILD_COMMAND}"
            "-E"
            "-W" #"-w" "build/doc/all/sphinx-warnings.txt"
            "-D" "project_builder=docx"
            "-D" "project_types=modules,files,modules2files"
            "-b" "docx"
            "doc"
            "build/doc/all/docx"
    COMMAND "${SPHINX_BUILD_COMMAND}"
            "-E"
            "-W" #"-w" "build/doc/all/sphinx-warnings.txt"
            "-D" "project_builder=pdf"
            "-D" "project_types=modules,files,modules2files"
            "-b" "pdf"
            "doc"
            "build/doc/all/pdf"
    DEPENDS "${SPHINX_BUILD_COMMAND}"
            "${PROJECT_SOURCE_DIR}/build/doxygen/main/xml/index.xml"
            "${PROJECT_SOURCE_DIR}/build/doxygen/main-no-group/xml/index.xml"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    USES_TERMINAL
    VERBATIM
)
add_custom_target("doc-modules"
    COMMAND "${CMAKE_COMMAND}" "-E" "rm" "-rf" "${PROJECT_SOURCE_DIR}/build/doc/modules"
    COMMAND "${SPHINX_BUILD_COMMAND}"
            "-E"
            "-W" #"-w" "build/doc/modules/sphinx-warnings.txt"
            "-D" "project_builder=docx"
            "-D" "project_types=modules"
            "-b" "docx"
            "doc"
            "build/doc/modules/docx"
    COMMAND "${SPHINX_BUILD_COMMAND}"
            "-E"
            "-W" #"-w" "build/doc/modules/sphinx-warnings.txt"
            "-D" "project_builder=pdf"
            "-D" "project_types=modules"
            "-b" "pdf"
            "doc"
            "build/doc/modules/pdf"
    DEPENDS "${SPHINX_BUILD_COMMAND}"
            "${PROJECT_SOURCE_DIR}/build/doxygen/main/xml/index.xml"
            "${PROJECT_SOURCE_DIR}/build/doxygen/main-no-group/xml/index.xml"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    USES_TERMINAL
    VERBATIM
)
add_custom_target("doc-files"
    COMMAND "${CMAKE_COMMAND}" "-E" "rm" "-rf" "${PROJECT_SOURCE_DIR}/build/doc/files"
    COMMAND "${SPHINX_BUILD_COMMAND}"
            "-E"
            "-W" #"-w" "build/doc/files/sphinx-warnings.txt"
            "-D" "project_builder=docx"
            "-D" "project_types=files"
            "-b" "docx"
            "doc"
            "build/doc/files/docx"
    COMMAND "${SPHINX_BUILD_COMMAND}"
            "-E"
            "-W" #"-w" "build/doc/files/sphinx-warnings.txt"
            "-D" "project_builder=pdf"
            "-D" "project_types=files"
            "-b" "pdf"
            "doc"
            "build/doc/files/pdf"
    DEPENDS "${SPHINX_BUILD_COMMAND}"
            "${PROJECT_SOURCE_DIR}/build/doxygen/main/xml/index.xml"
            "${PROJECT_SOURCE_DIR}/build/doxygen/main-no-group/xml/index.xml"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    USES_TERMINAL
    VERBATIM
)
add_custom_target("doc-modules2files"
    COMMAND "${CMAKE_COMMAND}" "-E" "rm" "-rf" "${PROJECT_SOURCE_DIR}/build/doc/modules2files"
    COMMAND "${SPHINX_BUILD_COMMAND}"
            "-E"
            "-W" #"-w" "build/doc/modules2files/sphinx-warnings.txt"
            "-D" "project_builder=docx"
            "-D" "project_types=modules2files"
            "-b" "docx"
            "doc"
            "build/doc/modules2files/docx"
    #[[COMMAND "${SPHINX_BUILD_COMMAND}"
            "-E"
            "-W" #"-w" "build/doc/modules2files/sphinx-warnings.txt"
            "-D" "project_builder=pdf"
            "-D" "project_types=modules2files"
            "-b" "pdf"
            "doc"
            "build/doc/modules2files/pdf"]]
    DEPENDS "${SPHINX_BUILD_COMMAND}"
            "${PROJECT_SOURCE_DIR}/build/doxygen/main/xml/index.xml"
            "${PROJECT_SOURCE_DIR}/build/doxygen/main-no-group/xml/index.xml"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    USES_TERMINAL
    VERBATIM
)
add_custom_target("doc"
    COMMAND "${CMAKE_COMMAND}" "-E" "rm" "-rf" "${PROJECT_SOURCE_DIR}/build/doc"
    COMMAND "${CMAKE_COMMAND}" "--build" "--preset" "${PRESET_NAME}" "--target" "doc-all"
    COMMAND "${CMAKE_COMMAND}" "--build" "--preset" "${PRESET_NAME}" "--target" "doc-modules"
    COMMAND "${CMAKE_COMMAND}" "--build" "--preset" "${PRESET_NAME}" "--target" "doc-files"
    COMMAND "${CMAKE_COMMAND}" "--build" "--preset" "${PRESET_NAME}" "--target" "doc-modules2files"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    USES_TERMINAL
    VERBATIM
)
add_custom_target("doc-clean"
    COMMAND "${CMAKE_COMMAND}" "-E" "rm" "-rf" "${PROJECT_SOURCE_DIR}/build/doc"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    USES_TERMINAL
    VERBATIM
)

set_target_names(ALL_TARGETS "${CMAKE_CURRENT_SOURCE_DIR}")
message(STATUS "all-targets:")
foreach(t IN LISTS ALL_TARGETS)
    message(STATUS "${t}")
endforeach()

set("${PROJECT_NAME}_ADDITIONAL_CLEAN_FILES"
    "${CMAKE_INSTALL_PREFIX}"
)
set_directory_properties(PROPERTIES
    ADDITIONAL_CLEAN_FILES "${${PROJECT_NAME}_ADDITIONAL_CLEAN_FILES}"
)
