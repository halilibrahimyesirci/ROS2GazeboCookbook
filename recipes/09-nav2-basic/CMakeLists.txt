cmake_minimum_required(VERSION 3.8)
project(rgc_nav2_basic)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY launch config rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
