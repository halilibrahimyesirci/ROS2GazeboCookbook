cmake_minimum_required(VERSION 3.8)
project(rgc_spawn_from_fuel)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY launch worlds config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
