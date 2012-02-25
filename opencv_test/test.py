
import numpy as np
import cv2
import sys

detector = cv2.SurfFeatureDetector()
extractor = cv2.DescriptorExtractor_create('SURF')

FLANN_INDEX_KDTREE = 1
FLANN_INDEX_LSH    = 6
flann_params= dict(algorithm = FLANN_INDEX_LSH,
                   table_number = 6, # 12
                   key_size = 12,     # 20
                   multi_probe_level = 1) #2
matcher = cv2.FlannBasedMatcher(flann_params, {})  # bug : need to pass empty dict (#1329)

green, red = (0, 255, 0), (0, 0, 255)


if __name__ == '__main__':

    # iterate over compare images
    # for each image:
    #    create matcher
    #    add descriptor to matcher      


    img = cv2.imread("sample_input.jpg")

    vis = img.copy()
    kp = detector.detect(img)
    kp, desc = extractor.compute(img, kp)

    ref_kp = kp

    for p in kp:
        x, y = np.int32(p.pt)
        r = int(0.5*p.size)
        cv2.circle(vis, (x, y), r, (0, 255, 0))
    
    if ref_kp is not None:
        raw_matches = matcher.knnMatch(desc, 2)
        matches = []
        for m in raw_matches:
            if len(m) == 2:
                m1, m2 = m
                if m1.distance < m2.distance * 0.7:
                    matches.append((m1.trainIdx, m1.queryIdx))
        match_n = len(matches)
    
    matcher.clear()
    matcher.add([desc])
