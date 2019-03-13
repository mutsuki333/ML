# opencv for cpp <!-- omit in toc -->

- [install & compile](#install--compile)
  - [Compile](#compile)

## install & compile

### Compile

setup pkgconfig
```shell
prefix=/usr/local
exec_prefix=${prefix}
includedir=${prefix}/include
libdir=${exec_prefix}/lib

Name: opencv
Description: The opencv library
Version: 4.0.1
Cflags: -I${includedir}/opencv -I${includedir}/opencv2
Libs: -L${libdir} -lopencv_calib3d \
-lopencv_core \
-lopencv_features2d \
-lopencv_flann \
-lopencv_highgui \
-lopencv_imgproc \
-lopencv_ml \
-lopencv_objdetect \
-lopencv_photo \
-lopencv_stitching \
-lopencv_video \
-lopencv_imgcodecs
```

compile by 
``` bash
g++ -std=c++11 `pkg-config opencv --cflags --libs` 
```