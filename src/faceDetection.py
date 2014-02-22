import cv2 as cv;
import sys

def crop_face(image):

    ## Attempts face detection, crops each face and then saves.
    ## Should support multiple faces.

    cropping_image = cv.imread(image)
    cascade = cv.LoadHaarClassifierCascade('haarcascade_frontalface_alt.xml',cv.size(1,1)) ## Need this file
    #cascade = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
    new_size = (img.shape[1],img.shape[0])
    new_frame = cv.resize(cropping_image,new_size)

    faces = cascade.detectMultiScale(new_frame)

    for i in faces:                                                      ## in case there is more than one face
        x,y,width,height = [v for v in i]
        cv.rectangle(cropping_image,(x,y),(x+width, y+height),(0,0,255)) ## creates a blue rectangle
        new_face = cropping_image[y:y+height, x:x+width]
        filenames = "face" + str(x) + ".jpg"                             ## eg: filename is "face90.jpg"
        cv.imwrite(filenames,new_face)
    return

def main():

    ## Saves an image from the webcam

    cv.NamedWindow("image stream", cv.WINDOW_AUTOSIZE)                 ## New window pops up
    image_capture = cv.videoCapture(0)                                 ## Not sure if this is the right function.
    cv.SetCaptureProperty(image_capture,cv.CAP_PROP_FRAME_WIDTH, 640)  ## Limits the height and width
    cv.SetCaptureProperty(image_capture,cv.CAP_PROP_FRAME_HEIGHT, 480) ## to 640 x 480.
    frame = cv.QueryFrame(image_capture)
    cv.ShowImage('image',frame)

    while(1):
        key = cv.WaitKey(100)
        if key == 0x20 ##  Waits until space is pressed.  0x1b for escape instead
            cv.imwrite('original.jpg', frame)
            break

    crop_face('original.jpg')

if __name__ == '__main__':


    main()
