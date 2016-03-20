# miningImageFeatures
Data mining project to mine the features of the images

1. How to compile OpenCV with extra modules ?
    - Download OpenCV and opencv\_contrib source code
	o wget https://github.com/Itseez/opencv/archive/3.1.0.zip
	o git clone https://github.com/Itseez/opencv_contrib

    - unzip 3.1.0.zip;	cd opencv-3.1.0; mkdir build; cd build
    
    - cmake -D OPENCV_EXTRA_MODULES_PATH=/mnt/extra/data_mining/opencv_contrib/modules /mnt/extra/data_mining/opencv-3.1.0/
    - make -j12
    - make install
    - export PYTHONPATH=/usr/local/lib/python2.7/dist-packages:$PYTHONPATH
	or
    - include PATH of cv2.so using sys.path()
