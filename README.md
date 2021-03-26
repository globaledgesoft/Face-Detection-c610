# Face Detection & Recognition on QCS610
The project is about detecting the person in a given frame. Images are captured from camera on live and shared for the prediction. After detecting the face, cropped face it will pass for the recognising target person. The project source tree contains 2 source files, 1 is for training the new person faces & another is for predicting on live stream. Local binary pattern histogram is used in this for recognising the face as Haar cascade classifier will perform the face detection.
                                                                           
## Dependencies
- Ubuntu System 18.04 or above
- Install Adb tool (Android debugging bridge) on host system
- Install opencv library on device


## Install opencv library on board 
- To install opencv library on the target board the required meta recipes for opencv is already present in folder “poky/meta-openembedded/meta-oe/ recipes-support/opencv/opencv_3.4.5.bb” file. We need to follow the below steps to build.

## Get into the yocto working directory
$ cd  <yocto working directory>
- Execute source command for environment setting 

 ```sh
 $ source poky/qti-conf/set_bb_env.sh
 ```

 - The pop up menu will be open for available machines that select “qcs610-odk” and press ok. Then one more pop up window will be open for distribution selection in that we need to select “qti-distro-fullstack-perf”  
Run the bitbake command for installing packages.

 ```sh
 $ bitbake opencv 
 ```

- Once the build is complete the shared library and include file will be available in “./tmp-glibc/sysroots-components/armv7ahf-neon/opencv/usr”
Push the opencv shared library to the target board 

 ```sh
 $ cd  ./tmp-glibc/sysroots-components/armv7ahf-neon/opencv/usr/
 $ adb push lib/  /data/face_recognition/
 ```
 ```
 Note : 
 For more reference refer to the “QCS610/QCS410 Linux Platform Development Kit Quick Start Guide document”.
 ```
- Also make sure install the all the dependency library from the yocto build to the system (ex: libgphoto2, libv4l-utils) 
bb recipes of above  library are available inside meta-oe layer you can directly run bitbake command

## Steps to run the application: 
         
 - To run application on the c610 board:

Remount the root directory writable: 

 ```sh
 $ adb root
 $ adb remount
 $ adb shell mount -o remount,rw /
 ```

## Push the source file on the target:
### Download the source repository
  
 ```sh
          $ git clone <source repository> 
          $ cd <Source_Dir>    
 ```

### Execute the application using below script for LBPH Training on host system:
 - Before running the training file, make sure you have stored images in ./images/ folder.

 - Images filename format should be as given, NAME##.ID.jpg. For example, John1.1.jpg, John2.1.jpg.

 - In the above file name example John is name and 1 is ID for that person.
Follow steps given below, if you have settled up with the training data.
           
 ```sh   
        $ cd /data/face_recognition/<Source_Dir>/
        $ python3.5 train.py
 ```
- Once LBPH Recognizer is trained, it will store the yml file inside the recognizer folder in the given project repository.     

### push the source file to the target board
 ```sh
     Push the source files to the target board
     $  adb push <Source_Dir>    /data/face_recognition
 ```           

### Run command given below for running recogniser.
    
 ```sh
    $ adb shell
    #/ cd /data/face_recognition/<Source_Dir>/
    Run the inference script   
    #/ python3.5 face_detector_recognizer.py
 ```
- It recognises the people in a given frame and draws it on the frame, and will write all the frame to video.mp4 in secondary.
