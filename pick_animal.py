import cv2, cv


image_path = "/Users/adamfletcher/Downloads/train/bw/"
image_extension = ".jpg"
image_prefix = "dog."
crop_target_directory = "cropped_images/"

def get_filename(index):
    return image_path + image_prefix + str(index) + image_extension

def load_checkpoint():
    try:
        checkpoint = open('dogs.checkpoint', 'r')
        starting_image = int(checkpoint.readline())
        print "Starting image: " + starting_image 
        checkpoint.close()
        return starting_image
    except:
        return 1

def on_mouse(event, x, y, flags, params):
    draw = False
    images_metadata = params[0]
    filename = params[1]
    img = params[2]
    if event == cv.CV_EVENT_LBUTTONDOWN:
        print 'Start Mouse Position: '+str(x)+', '+str(y)
        p1 = [x, y]
        if p1 != images_metadata[filename]['p1']: 
            images_metadata[filename]['p1'] = p1
            draw = True
    elif event == cv.CV_EVENT_LBUTTONUP:
        print 'End Mouse Position: '+str(x)+', '+str(y)
        p2 = [x, y]
        if p2 != images_metadata[filename]['p2']: 
            images_metadata[filename]['p2'] = p2
            draw = True
    if draw:
        draw_box(img, images_metadata, filename)

def draw_box(img, images_metadata, filename):
    if len(images_metadata[filename]['p1']) == 2 and len(images_metadata[filename]['p2']) == 2:
        cv2.rectangle(img, (images_metadata[filename]['p1'][0], images_metadata[filename]['p1'][1]), 
                          (images_metadata[filename]['p2'][0], images_metadata[filename]['p2'][1]), (155, 55, 200), 2)
        cv2.imshow("Image", img)


def mark_images(image_count, images_metadata):
    count = image_count
    while(count < 10000):
        filename = get_filename(count) 
        img = cv2.imread(filename)
        images_metadata[filename] = {}
        images_metadata[filename]['p1'] = []
        images_metadata[filename]['p2'] = []

        cv2.namedWindow("Image")
        cv.SetMouseCallback("Image", on_mouse, [images_metadata, filename, img])
        cv2.putText(img, str(count), (1,20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))
        cv2.imshow("Image", img)
        key = cv2.waitKey(0)
        if len(images_metadata[filename]['p1']) == 2 and len(images_metadata[filename]['p2']) == 2:
            write_metadata(count, filename, images_metadata)
        if key == 27:
            cv2.destroyAllWindows()
            return count
        count += 1

def write_metadata(image_index, filename, images_metadata):
    if len(images_metadata[filename]['p1']) == 2 and len(images_metadata[filename]['p2']) == 2:
        datafile = open('dogs.dat', 'a+')
        # the opencv classifier wants x, y, width, height with x,y being the upper left corner
        p1 = images_metadata[filename]['p1']
        p2 = images_metadata[filename]['p2']
        width = p2[0] - p1[0]
        height = p2[1] - p1[1]
        x = p1[0]
        y = p1[1]
        if(width < 0 or height < 0):
            x = p2[0]
            y = p2[1]
        width = abs(width)
        height = abs(height)
        print filename, x, y, width, height 
        datafile.write("%s 1 %i %i %i %i\n" % (filename, x, y, width, height))
        checkpoint(image_index)
        datafile.close()

def checkpoint(image_index):
    checkpoint = open('dogs.checkpoint', 'w')
    checkpoint.write("%i" % image_index)
    checkpoint.close()


starting_image = load_checkpoint()
images_metadata = {}
ending_image = mark_images(starting_image, images_metadata)

