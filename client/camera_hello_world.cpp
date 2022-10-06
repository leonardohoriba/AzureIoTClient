#include <iostream>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/video.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
//#include "detector.h"
//#include "poseEstimation.h"
using namespace cv;

std::string gstreamer_pipeline(int capture_width, int capture_height, int framerate, int display_width, int display_height) {
    return
            " libcamerasrc ! video/x-raw, "
            " width=(int)" + std::to_string(capture_width) + ","
            " height=(int)" + std::to_string(capture_height) + ","
            " framerate=(fraction)" + std::to_string(framerate) +"/1 !"
            " videoconvert ! videoscale !"
            " video/x-raw,"
            " width=(int)" + std::to_string(display_width) + ","
            " height=(int)" + std::to_string(display_height) + " ! appsink";
}

int main()
{
    //pipeline parameters
    int capture_width = 640; //1280 ;
    int capture_height = 480; //720 ;
    int framerate = 15 ;
    int display_width = 640; //1280 ;
    int display_height = 480; //720 ;

    //reset frame average
    std::string pipeline = gstreamer_pipeline(capture_width, capture_height, framerate,
                                              display_width, display_height);
    std::cout << "Using pipeline: \n\t" << pipeline << "\n\n\n";

    VideoCapture cap(pipeline, cv::CAP_GSTREAMER);
    if(!cap.isOpened()) {
        std::cout<<"Failed to open camera."<<std::endl;
        return (-1);
    }

    namedWindow("Camera", cv::WINDOW_AUTOSIZE);
//VideoCapture cap(0, cv::CAP_MSMF);
//VideoCapture cap("C:/www/town.avi", cv::CAP_MSMF);
VideoWriter writer;
/*
OLD RTSP pipeline
writer.open("appsrc ! videoconvert ! videoscale ! video/x-raw,width=640,height=480 ! x264enc speed-preset=veryfast tune=zerolatency bitrate=640 ! rtspclientsink location=rtsp://localhost:8554/mystream ",0,10,Size(640, 480),true);
*/

//NEW RTMP2SINK pipeline
//writer.open("videotestsrc ! videoconvert ! videoscale ! video/x-raw,width=640,height=480 ! x264enc ! flvmux ! rtmp2sink location=rtmp://x.rtmp.youtube.com/live2/ect7-wqu9-tpce-qp22-d81u", 0, 10, Size(640, 480), true);
writer.open("videotestsrc is-live=1 ! videoconvert ! video/x-raw, width=1280, height=720, framerate=25/1 ! queue ! x264enc bitrate=2000 byte-stream=false key-int-max=60 bframes=0 aud=true tune=zerolatency ! video/x-h264,profile=main ! flvmux streamable=true name=mux ! rtmpsink location=\"rtmp://x.rtmp.youtube.com/live2/ect7-wqu9-tpce-qp22-d81u app=live2\" audiotestsrc ! voaacenc bitrate=128000 ! mux. ", 0, 10, Size(640, 480), true);
/*
poseEstimation pose = poseEstimation();
Detector dec = Detector();
*/
Mat img;
for (;;) {
  //cap.read(img); 
  /*dec.ProcessFrame(img);
  dec.detect();
  Mat proc = dec.getResult();
  pose.ProcessFrame(proc);
  pose.drawResults();
  */
  if (!cap.read(img)) {
            std::cout<<"Capture read error"<<std::endl;
            break;
        }
        //show frame
        imshow("Camera",img);
  writer << img;
  cv::waitKey(25);
  }
}