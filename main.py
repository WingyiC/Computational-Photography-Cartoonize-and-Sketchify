import errno
import os
import sys

import numpy as np
import cv2

from glob import glob
import finalProject as fp


def readImages(image_dir):
    extensions = ['bmp', 'pbm', 'pgm', 'ppm', 'sr', 'ras', 'jpeg',
                  'jpg', 'jpe', 'jp2', 'tiff', 'tif', 'png']

    search_paths = [os.path.join(image_dir, '*.' + ext) for ext in extensions]
    image_files = sorted(reduce(list.__add__, map(glob, search_paths)))
    images = [cv2.imread(f, cv2.IMREAD_UNCHANGED | cv2.IMREAD_COLOR)
              for f in image_files]

    bad_read = any([img is None for img in images])
    if bad_read:
        raise RuntimeError(
            "Reading one or more files in {} failed - aborting."
            .format(image_dir))

    return images


if __name__ == "__main__":
    video_dir = "house"
    image_dir = os.path.join("videos", "source", video_dir)
    out_dir = os.path.join("videos", "out")

    try:
        _out_dir = os.path.join(out_dir, video_dir)
        not_empty = not all([os.path.isdir(x) for x in
                             glob(os.path.join(_out_dir, "*.*"))])
        if not_empty:
            raise RuntimeError("Output directory is not empty - aborting.")
        os.makedirs(_out_dir)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    '''
    Apply Cartoonize and Sketchify to video, run these lines of code!!!
    print "Reading images."
    images = readImages(image_dir)
    out_list = fp.SketchifyVideo(images)

    for idx, image in enumerate(out_list):
        cv2.imwrite(os.path.join(out_dir, video_dir,
                    'frame{0:04d}.png'.format(idx)), image)
    '''

    inputImg = cv2.imread("test4.jpg")
    SmoothImg = fp.SmoothImages(inputImg, 7, 15) #blurriness can be change
    edgeMask = fp.GetEdgeMask(SmoothImg)
    DilatedEdges = fp.EdgesDilation(edgeMask, 4) #thickness can be change
    ToonifiedImg = fp.Toonify(SmoothImg,DilatedEdges)
    cv2.imwrite("B4_Toonified.jpg", ToonifiedImg)

    grayScaleImg = fp.getGrayScale(inputImg)
    negativeImg = fp.getNegative(grayScaleImg)
    sketchMask = fp.getSketchMask(negativeImg, 11) #kSize can be change
    SketchifiedImg = fp.Sketchify(grayScaleImg, sketchMask, 258) #darkness can be change
    cv2.imwrite("A4_Sketchified.jpg", SketchifiedImg)
