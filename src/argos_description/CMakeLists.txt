cmake_minimum_required(VERSION 3.8)
project(argos_description)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY
    launch
    models
    worlds
  DESTINATION share/${PROJECT_NAME}
  PATTERN "__pycache__" EXCLUDE
  PATTERN "*.pyc" EXCLUDE
)

ament_package()
