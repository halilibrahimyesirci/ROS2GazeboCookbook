cmake_minimum_required(VERSION 3.8)
project(rgc_reference_robot)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY launch worlds models config rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
