import cv2, cv

starting_image = 1
try:
   checkpoint = open('dogs.checkpoint', 'r')
   starting_image = int(checkpoint.readline())
   print starting_image 
   checkpoint.close()
except:
    starting_image = 1


boxes = {}
def on_mouse(event, x, y, flags, params):
    draw = False
    if event == cv.CV_EVENT_LBUTTONDOWN:
        print 'Start Mouse Position: '+str(x)+', '+str(y)
        p1 = [x, y]
        if p1 != boxes[filename]['p1']: 
            boxes[filename]['p1'] = p1
            draw = True
    elif event == cv.CV_EVENT_LBUTTONUP:
        print 'End Mouse Position: '+str(x)+', '+str(y)
        p2 = [x, y]
        if p2 != boxes[filename]['p2']: 
            boxes[filename]['p2'] = p2
            draw = True
    if draw:
        drawBox()

def drawBox():
    if len(boxes[filename]['p1']) == 2 and len(boxes[filename]['p2']) == 2:
    #    print "drawing"
        cv2.rectangle(img, (boxes[filename]['p1'][0], boxes[filename]['p1'][1]), 
                          (boxes[filename]['p2'][0], boxes[filename]['p2'][1]), (155, 55, 200), 2)
        cv2.imshow('real image', img)
    #    print filename, boxes[filename]['p1'][0], boxes[filename]['p1'][1], boxes[filename]['p2'][0], boxes[filename]['p2'][1]

count = starting_image
filename = ''
img = cv2.imread(filename)
while(count < 100):
    filename = '/Users/adamfletcher/Downloads/train/dog.' + str(count) + '.jpg'
    img = cv2.imread(filename)
    boxes[filename] = {}
    boxes[filename]['p1'] = []
    boxes[filename]['p2'] = []

    cv2.namedWindow('real image')
    cv.SetMouseCallback('real image', on_mouse, 0)
    cv2.imshow('real image', img)
    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()
        break
    count += 1


datafile = open('dogs.dat', 'a+')
for filename in boxes.keys():
    if len(boxes[filename]['p1']) == 2 and len(boxes[filename]['p2']) == 2:
        # the opencv classifier wants x, y, width, height with x,y being the upper left corner
        p1 = boxes[filename]['p1']
        p2 = boxes[filename]['p2']
        width = p2[0] - p1[0]
        height = p2[1] - p1[1]
        x = p1[0]
        y = p1[1]
        if(width < 0 or height < 0):
            x = p2[0]
            y = p2[1]
        width = abs(width)
        height = abs(height)
        starting_image = starting_image + 1
        print filename, x, y, width, height 
        datafile.write("%s 1 %i %i %i %i\n" % (filename, x, y, width, height))

datafile.close()

checkpoint = open('dogs.checkpoint', 'w')
checkpoint.write("%i" % starting_image)
checkpoint.close()


