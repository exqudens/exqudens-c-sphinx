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
    OUTPUT "${PROJECT_BINARY_DIR}/doxygen/main/xml/index.xml"
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
    OUTPUT "${PROJECT_BINARY_DIR}/doxygen/main-no-group/xml/index.xml"
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

add_custom_target("doc-modules"
    COMMAND "${CMAKE_COMMAND}" "-P" "${CMAKE_UTIL_FILE}" "--" "sphinx"
            SOURCE_BASE_DIR "${PROJECT_SOURCE_DIR}"
            BUILD_DIR "build/sphinx"
            CONF_JSON_VARS "PROJECT_DIR=${PROJECT_SOURCE_DIR}"
                           #"PROJECT_BREATHE_DEFAULT=main"
                           "PROJECT_TITLE=${PROJECT_NAME} modules"
                           "PROJECT_STYLE_DOCX=${PROJECT_SOURCE_DIR}/doc/style.docx"
            OUTPUT_DIR "build/doc/modules"
            TYPE "modules"
            FILES "modules/modules.rst"
            EXTRA_FILES "conf_util.py"
            BUILDERS "docx"
            WARNINGS_TO_ERRORS "1"
            #SPHINX_WARNINGS_ERRORS_FILE "build/doc/modules/sphinx-warnings.txt"
    DEPENDS "${PROJECT_BINARY_DIR}/doxygen/main/xml/index.xml"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    VERBATIM
    USES_TERMINAL
)
add_custom_target("doc-files"
    COMMAND "${CMAKE_COMMAND}" "-P" "${CMAKE_UTIL_FILE}" "--" "sphinx"
            SOURCE_BASE_DIR "${PROJECT_SOURCE_DIR}"
            BUILD_DIR "build/sphinx"
            CONF_JSON_VARS "PROJECT_DIR=${PROJECT_SOURCE_DIR}"
                           #"PROJECT_BREATHE_DEFAULT=main"
                           "PROJECT_TITLE=${PROJECT_NAME} files"
                           "PROJECT_STYLE_DOCX=${PROJECT_SOURCE_DIR}/doc/style.docx"
            OUTPUT_DIR "build/doc/files"
            TYPE "files"
            FILES "files/files.rst"
            EXTRA_FILES "conf_util.py"
            BUILDERS "docx"
            WARNINGS_TO_ERRORS "1"
            #SPHINX_WARNINGS_ERRORS_FILE "build/doc/files/sphinx-warnings.txt"
    DEPENDS "${PROJECT_BINARY_DIR}/doxygen/main-no-group/xml/index.xml"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    VERBATIM
    USES_TERMINAL
)
add_custom_target("doc-modules2files"
    COMMAND "${CMAKE_COMMAND}" "-P" "${CMAKE_UTIL_FILE}" "--" "sphinx"
            SOURCE_BASE_DIR "${PROJECT_SOURCE_DIR}"
            BUILD_DIR "build/sphinx"
            CONF_JSON_VARS "PROJECT_DIR=${PROJECT_SOURCE_DIR}"
                           #"PROJECT_BREATHE_DEFAULT=main"
                           "PROJECT_TITLE=${PROJECT_NAME} modules2files"
                           "PROJECT_STYLE_DOCX=${PROJECT_SOURCE_DIR}/doc/style.docx"
                           "PROJECT_RST_MAIN=modules2files/modules2files"
            OUTPUT_DIR "build/doc/modules2files"
            TYPE "modules2files"
            TOCTREE_HIDDEN "1"
            FILES "modules2files/modules2files.rst"
                  "modules/modules.rst"
                  "files/files.rst"
            EXTRA_FILES "conf_util.py"
            BUILDERS "docx"
            WARNINGS_TO_ERRORS "0"
            SPHINX_WARNINGS_ERRORS_FILE "build/doc/modules2files/sphinx-warnings.txt"
    DEPENDS "${PROJECT_BINARY_DIR}/doxygen/main/xml/index.xml"
            "${PROJECT_BINARY_DIR}/doxygen/main-no-group/xml/index.xml"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    VERBATIM
    USES_TERMINAL
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
