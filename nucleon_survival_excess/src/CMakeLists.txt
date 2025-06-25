cmake_minimum_required(VERSION 3.1.0 FATAL_ERROR)
project(
    hepmc3reader
  VERSION 1.0
  LANGUAGES CXX)

set(CMAKE_BUILD_TYPE Debug)


find_package(ROOT 6.16 CONFIG REQUIRED)
find_package(NEUT)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

include(GNUInstallDirs)
include(CheckCXXCompilerFlag)

set(SOURCES1 ${CMAKE_CURRENT_SOURCE_DIR}/nucleon_survival_excess_gen.cpp ${CMAKE_CURRENT_SOURCE_DIR}/is_alive.cpp
${CMAKE_CURRENT_SOURCE_DIR}/ratio_histo.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/is_alive.h)

add_executable(nucleon_survival_excess_gen ${SOURCES1})

target_link_libraries(nucleon_survival_excess_gen ROOT::Core ROOT::Hist NEUT::All)
