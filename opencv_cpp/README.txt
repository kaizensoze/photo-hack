To run this sample you need:
1. CMake
2. OpenCV 2.3.1 unpacked somewhere

How to build:
A. Build OpenCV. 
    1. Go to the OpenCV source directory, run `cmake -D CMAKE_BUILD_TYPE=RELEASE .'
    2. Run `make'
    3. Wait.
B. Build the sample.
    1. Go to photo-hack/opencv_cpp/
    2. Run `cmake -D OpenCV_DIR=<path to OpenCV source dir> .'
    3. Run `make'.

How to run:
Specify the images as command line arguments. First image is the query image, the rest are candidates.

Example:

$ ./SURF_FlannMatcher low1.jpg capitol1.jpg low2.jpg hoover1.jpg es1.jpg 
Loading query image: low1.jpg
Query image loaded successfully.
Loaded 4 candidate images.
Detecting key points.
Extracting descriptors.
RUNNING MATCHER.
-- Max dist : 0.675288 
-- Min dist : 0.074248 
Getting best image.
Winning image: low2.jpg
Scores: 1 29 9 2
