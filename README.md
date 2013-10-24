DogsAndCats
===========

OpenCV dogs &amp; cats recognizer

example invocation:

python2.7 pick_animal.py --image_prefix dog. --metadata_filename dogs.dat --image_path /Users/adamfletcher/Downloads/train/bw/ --aspect_ratio 1 --target_path cropped/ --resize_to_width 240

Requires OpenCV 2.4; if you're on OS X the best bet is to use MacPorts to install it:

sudo port install opencv +python2.7 +tbb

You really, really want +tbb to make sure you tools end up multithreaded.
