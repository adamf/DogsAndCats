import cv2, cv


good_eyes = open('dog_eyes.dat', 'w')
DOWNSCALE = 1
classifier = cv2.CascadeClassifier("trained/cascade.xml")
#classifier = cv2.CascadeClassifier("/opt/local/share/OpenCV/haarcascades/haarcascade_eye.xml")
#classifier = cv2.CascadeClassifier("/opt/local/share/OpenCV/haarcascades/haarcascade_mcs_eyepair_big.xml")
#classifier = cv2.CascadeClassifier("/opt/local/share/OpenCV/haarcascades/haarcascade_mcs_eyepair_small.xml")
for count in range(1,1000):
    filename = '/Users/adamfletcher/Downloads/train/bw/cat.' + str(count) + '.jpg'
    img = cv2.imread(filename)
    dogs = classifier.detectMultiScale(img)


    if len(dogs) > 1:
        print dogs[0]
        i = 0
        for d in dogs:
            x, y, w, h  = [ v*DOWNSCALE for v in d ]
            cv2.putText(img, str(i), (x,y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255))
            i = i + 1
        cv2.imshow("dog", img)
        key = cv2.waitKey(0)
        if key == 107:
            # we have a good eye match
            good_eyes.write(filename + '\n')
            print filename
        print key
        if key == 27:
            break

good_eyes.close()
