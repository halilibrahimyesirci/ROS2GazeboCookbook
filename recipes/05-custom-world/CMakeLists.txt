cmake_minimum_required(VERSION 3.8)
project(rgc_custom_world)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY launch worlds models config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
