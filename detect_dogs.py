import cv2, cv



DOWNSCALE = 1
#classifier = cv2.CascadeClassifier("trained/cascade.xml")
#classifier = cv2.CascadeClassifier("/opt/local/share/OpenCV/haarcascades/haarcascade_eye.xml")
#classifier = cv2.CascadeClassifier("/opt/local/share/OpenCV/haarcascades/haarcascade_mcs_eyepair_big.xml")
classifier = cv2.CascadeClassifier("/opt/local/share/OpenCV/haarcascades/haarcascade_mcs_eyepair_small.xml")
for count in range(1,23):
    filename = '/Users/adamfletcher/Downloads/train/dog.' + str(count) + '.jpg'
    img = cv2.imread(filename)
    dogs = classifier.detectMultiScale(img)


    for f in dogs:
        print f
        x, y, w, h = [ v*DOWNSCALE for v in f ]
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255))
    cv2.imshow("dog", img)
    key = cv2.waitKey(0)

