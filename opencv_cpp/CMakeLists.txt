project( SURF_FlannMatcher )
find_package( OpenCV REQUIRED )
add_executable( SURF_FlannMatcher SURF_FlannMatcher )
target_link_libraries( SURF_FlannMatcher ${OpenCV_LIBS} )
