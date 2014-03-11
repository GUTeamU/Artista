import cv
import time

HAAR_CASCADE_PATH = "/home/clopema/catkin_clopema/src/TP3-Artista/haarcascade_frontalface_alt.xml"
X_RES = 640
Y_RES = 480
X_OFFSET = (int)( 0.1 * X_RES)
Y_OFFSET = (int)( 0.1 * Y_RES)
PREVIOUS = 0

def detect_faces(image):
    global PREVIOUS

    faces = []
    detected = cv.HaarDetectObjects(image, cascade, storage, 1.1, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (100,100))
    if detected:
        if(len(detected)!=PREVIOUS):
            print "Detected " + str(len(detected)) + " faces."
        PREVIOUS = len(detected)
        for (x,y,w,h),n in detected:
            faces.append((x-X_OFFSET,y-Y_OFFSET,w+X_OFFSET*2,h+Y_OFFSET*2))
            
        
            
    return faces

def take_Picture(path):
    image_capture = cv.CreateCameraCapture(0)
    cv.SetCaptureProperty(image_capture, cv.CV_CAP_PROP_FRAME_WIDTH, X_RES)
    cv.SetCaptureProperty(image_capture, cv.CV_CAP_PROP_FRAME_HEIGHT, Y_RES)

    storage = cv.CreateMemStorage()
    cascade = cv.Load(HAAR_CASCADE_PATH)
    faces = []

    
    while (1):
        frame = cv.QueryFrame(image_capture)
        cv.ShowImage('image',frame)
        key = cv.WaitKey(1)

        faces = detect_faces(frame)

        for (x,y,w,h) in faces:
            cv.Rectangle(frame, (x,y), (x+w,y+h), (0,0,0))
        key = cv.WaitKey(1)
        
        if key == 1048608: ## If the space bar is pressed. Image will be save.
            print "key pressed"
            ## start of cropping images
            print str(key)
            for f in faces:
                x = f[0]
                y = f[1]
                w = f[2]
                h = f[3]


                sub_face = frame[y:y+h, x:x+w]
                filename = path + "temp.jpg"
                print "Saving image to: " + filename
                cv.SaveImage(filename,sub_face)
            # cv.SaveImage(str(ts)+'.jpg', frame)

            break
        #new

if __name__ == "__main__":
    image_capture = cv.CreateCameraCapture(0)
    cv.SetCaptureProperty(image_capture, cv.CV_CAP_PROP_FRAME_WIDTH, X_RES)
    cv.SetCaptureProperty(image_capture, cv.CV_CAP_PROP_FRAME_HEIGHT, Y_RES)

    storage = cv.CreateMemStorage()
    cascade = cv.Load(HAAR_CASCADE_PATH)
    faces = []

    
    while (1):
        frame = cv.QueryFrame(image_capture)
        cv.ShowImage('image',frame)
        key = cv.WaitKey(1)

        faces = detect_faces(frame)

        for (x,y,w,h) in faces:
            cv.Rectangle(frame, (x,y), (x+w,y+h), (0,0,0))
        key = cv.WaitKey(1)
        
        if key == 1048608: ## If the space bar is pressed. Image will be save.
            print "key pressed"
            ## start of cropping images
            print str(key)
            for f in faces:
                x = f[0]
                y = f[1]
                w = f[2]
                h = f[3]


                sub_face = frame[y:y+h, x:x+w]
                filename ="./pictures/" + "face" + str(y)  + ".jpg"
                print "saving image to: " + filename
                cv.SaveImage(filename,sub_face)
            # cv.SaveImage(str(ts)+'.jpg', frame)

            break
        #new

        
