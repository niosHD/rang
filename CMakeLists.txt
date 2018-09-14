cmake_minimum_required (VERSION 3.0.0)

# parse the current version from the rang header
file(STRINGS "${CMAKE_CURRENT_SOURCE_DIR}/include/rang.hpp" rang_version_defines
     REGEX "#define RANG_VERSION_")
foreach(line ${rang_version_defines})
  if(line MATCHES "#define RANG_VERSION_(MAJOR|MINOR|PATCH) +([^ ]+) *$")
    set(${CMAKE_MATCH_1} "${CMAKE_MATCH_2}")
  endif()
endforeach()

project (rang VERSION "${MAJOR}.${MINOR}.${PATCH}" LANGUAGES CXX)

add_library(rang INTERFACE)
add_library(rang::rang ALIAS rang)
target_include_directories(rang INTERFACE $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
                                          $<INSTALL_INTERFACE:include>)
target_compile_features(rang INTERFACE cxx_std_11)

# Determine if project is built as a subproject (using add_subdirectory)
# or if it is the master project.
if (PROJECT_NAME STREQUAL CMAKE_PROJECT_NAME)
#   # TODO Port building and running the tests to CMake if needed.
#   enable_testing()
#   option(BUILD_TESTS "Build tests by default." ON)
#   if(BUILD_TESTS)
#     add_subdirectory(ELFIOTest)
#   else()
#     add_subdirectory(ELFIOTest EXCLUDE_FROM_ALL)
#   endif()

  #----------------------------------------------------------------------------
  # Installation and export configuration
  #----------------------------------------------------------------------------
  # Setup variables with the paths and targets that should be installed.
  # Using cached variables to permit overriding them from the command line.
  include(GNUInstallDirs)
  set(CONFIG_FILE_INSTALL_DIR "${CMAKE_INSTALL_LIBDIR}/cmake/rang" CACHE STRING
      "Installation directory for cmake files, relative to CMAKE_INSTALL_PREFIX.")
  set(LIB_INSTALL_DIR "${CMAKE_INSTALL_LIBDIR}" CACHE STRING
      "Installation directory for libraries, relative to CMAKE_INSTALL_PREFIX.")
  set(INCLUDE_INSTALL_DIR "${CMAKE_INSTALL_INCLUDEDIR}" CACHE STRING
      "Installation directory for include files, relative to CMAKE_INSTALL_PREFIX.")

  set(version_config "${PROJECT_BINARY_DIR}/rang-config-version.cmake")
  set(project_config "${PROJECT_BINARY_DIR}/rang-config.cmake")
  set(targets_export_name "rang-targets")
  set(install_targets "rang")
  set(namespace "rang::")

  # Generate the version, config and target files into the build directory.
  include(CMakePackageConfigHelpers)
  write_basic_package_version_file("${version_config}"
                                   VERSION "${PROJECT_VERSION}"
                                   COMPATIBILITY "AnyNewerVersion")
  configure_package_config_file("${PROJECT_SOURCE_DIR}/rang-config.cmake.in"
                                "${project_config}"
                                INSTALL_DESTINATION "${CONFIG_FILE_INSTALL_DIR}")
  export(TARGETS ${install_targets}
         NAMESPACE "${namespace}"
         FILE "${PROJECT_BINARY_DIR}/${targets_export_name}.cmake")

  # Install version, config and target files.
  install(FILES "${project_config}" "${version_config}"
          DESTINATION "${CONFIG_FILE_INSTALL_DIR}")
  install(EXPORT "${targets_export_name}"
          DESTINATION "${CONFIG_FILE_INSTALL_DIR}"
          NAMESPACE "${namespace}")

  # Install the library and headers.
  install(TARGETS ${install_targets}
          EXPORT "${targets_export_name}"
          DESTINATION "${LIB_INSTALL_DIR}")
  install(FILES "include/rang.hpp"
          DESTINATION "${INCLUDE_INSTALL_DIR}")

  #----------------------------------------------------------------------------
  # Simple packaging support
  #----------------------------------------------------------------------------
  set(CPACK_PACKAGE_VERSION_MAJOR "${PROJECT_VERSION_MAJOR}")
  set(CPACK_PACKAGE_VERSION_MINOR "${PROJECT_VERSION_MINOR}")
  set(CPACK_PACKAGE_VERSION_PATCH "${PROJECT_VERSION_PATCH}")
  set(CPACK_SOURCE_GENERATOR ZIP)
  set(CPACK_SOURCE_PACKAGE_FILE_NAME "rang-${PROJECT_VERSION}")
  set(CPACK_RESOURCE_FILE_README "${PROJECT_SOURCE_DIR}/README.md")
  set(CPACK_RESOURCE_FILE_LICENSE "${PROJECT_SOURCE_DIR}/LICENSE")
  set(CPACK_PACKAGE_NAME "rang")
  include(CPack)
endif ()
