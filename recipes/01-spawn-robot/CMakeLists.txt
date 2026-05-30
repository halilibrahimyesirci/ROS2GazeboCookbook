cmake_minimum_required(VERSION 3.8)
project(rgc_spawn_robot)

find_package(ament_cmake REQUIRED)

# This package ships only data (worlds, models, launch, config); there is
# nothing to compile. Install the asset directories into the package share.
install(
  DIRECTORY launch worlds models config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
