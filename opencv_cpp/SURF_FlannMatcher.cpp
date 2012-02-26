/**
 * @file SURF_FlannMatcher
 * @brief SURF detector + descriptor + FLANN Matcher
 * @author A. Huaman
 */

#include <stdio.h>
#include <iostream>
#include "opencv2/core/core.hpp"
#include "opencv2/features2d/features2d.hpp"
#include "opencv2/highgui/highgui.hpp"

using namespace cv;

void readme();

/**
 * @function main
 * @brief Main function
 */
int main( int argc, char** argv )
{
	if( argc < 3 )
	{ readme(); return -1; }

	std::cout << "Loading query image: " << argv[1] << std::endl;
	Mat image_query = imread(argv[1], CV_LOAD_IMAGE_GRAYSCALE);
	if( !image_query.data ) { std::cout<< " --(!) Error reading query image. " << std::endl; return -1; }
	std::cout << "Query image loaded successfully." << std::endl;

	std::vector<Mat> image_db;
	std::vector<char*> filename_db;
	for (int imgId = 2; imgId < argc; imgId++) {
		Mat img_i = imread( argv[imgId], CV_LOAD_IMAGE_GRAYSCALE );
		if( !img_i.data ) { std::cout<< " --(!) Error reading images " << std::endl; return -1; }
		image_db.push_back(img_i);
		filename_db.push_back(argv[imgId]);
	}
	std::cout << "Loaded " << (int) image_db.size() << " candidate images." << std::endl;

	//-- Step 1: Detect the keypoints using SURF Detector
	int minHessian = 400;
	SurfFeatureDetector detector( minHessian );

	std::vector< KeyPoint > keypoints_query;
	std::vector< std::vector< KeyPoint > > keypoints_db;

	std::cout << "Detecting key points." << std::endl;
	detector.detect( image_query, keypoints_query );
	for (int imgId = 0; imgId < image_db.size(); imgId++) {
		std::vector<KeyPoint> keypoints_i;
		detector.detect( image_db[imgId], keypoints_i );
		keypoints_db.push_back(keypoints_i);
	}

	//-- Step 2: Calculate descriptors (feature vectors)
	std::cout << "Extracting descriptors." << std::endl;
	SurfDescriptorExtractor extractor;

	Mat descriptors_query;
	std::vector<Mat> descriptors_db;

	extractor.compute( image_query, keypoints_query, descriptors_query );
	for (int imgId = 0; imgId < image_db.size(); imgId++) {
		Mat descriptors_i;
		extractor.compute( image_db[imgId], keypoints_db[imgId], descriptors_i );
		descriptors_db.push_back(descriptors_i);
	}

	//-- Step 3: Matching descriptor vectors using FLANN matcher
	FlannBasedMatcher matcher;
	matcher.add(descriptors_db);
	// matcher.train(); // In all methods to match, the method train() is run every time before matching. 

	std::vector< DMatch > matches;
	std::cout << "RUNNING MATCHER." << std::endl;
	matcher.match( descriptors_query, matches ); // get all matches

	double max_dist = 0; double min_dist = 100;

	//-- Quick calculation of max and min distances between keypoints
	for( int i = 0; i < matches.size(); i++ )
	{ double dist = matches[i].distance;
		if( dist < min_dist ) min_dist = dist;
		if( dist > max_dist ) max_dist = dist;
	}

	printf("-- Max dist : %f \n", max_dist );
	printf("-- Min dist : %f \n", min_dist );

	std::vector< int > scores_db;
	for (int imgId = 0; imgId < image_db.size(); imgId++) {
		scores_db.push_back(0);
	}
	//-- PS.- radiusMatch can also be used here.
	//std::vector< DMatch > good_matches;

	std::cout << "Getting best image." << std::endl;
	int max_score = 0;
	int max_scorer = -1;
	for( int i = 0; i < matches.size(); i++ ) {
		if( matches[i].distance <= 2*min_dist ) {
			// got one!
			int imgId = matches[i].imgIdx;
			int score = ++scores_db[imgId];
			if (score > max_score) {
				max_score = score;
				max_scorer = imgId;
			}
		}
	}  

	if (max_scorer >= 0) {
		std::cout << "Winning image: " << filename_db[max_scorer] << std::endl;
		std::cout << "Scores: ";
		for ( int i = 0; i < scores_db.size(); i++ ) {
			std::cout << scores_db[i] << " ";
		}
		std::cout << std::endl;
	} else {
		std::cout << "Results are inconclusive." << std::endl;
	}

	return 0;
}

/**
 * @function readme
 */
void readme()
{ std::cout << " Usage: ./SURF_FlannMatcher <queryimg> <img1> <img2> ... <imgn>" << std::endl; }
