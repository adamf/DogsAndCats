import argparse
import cv2, cv

parser = argparse.ArgumentParser(
    description='Image manipulator for computer vision positive sample creation.')

parser.add_argument('--image_path', dest='image_path', default='.',
                    help='Directory containing the images to process (default: .).')

parser.add_argument('--image_prefix', dest='image_prefix', required=True,
                    help='Prefix for images to process, eg for a set of images '
                         'dog1.jpg through dog1000.jpg, --image_prefix should be "dog"')

parser.add_argument('--image_extension', dest='image_extension', default='.jpg',
                    help='Filename extension for images to process (default: .jpg).')

parser.add_argument('--target_path', dest='target_path', default='.',
                    help='Directory in which to store the processed images and metadata (default: .).')

parser.add_argument('--metadata_filename', dest='metadata_filename', required=True,
                    help='Filename to use for the processed image metadata.')

parser.add_argument('--overwrite_metadata', dest='overwrite_metadata', default=False,
                    help='If set, overwrite any existing metadata.')

# We'll try to normalize the captured images' aspect ratio to a fixed ratio; later we can scale them all
# to the same size. The normalization will only increase the size of the capture, never shrink it. By default
# we seek to capture a square. For human faces, which are taller than they are long, a square is probably not
# the best ratio. 
parser.add_argument('--aspect_ratio_width', dest='aspect_ratio_width', default=1,
                    help='Default width aspect ratio value for image size normalization (default:1)')

parser.add_argument('--aspect_ratio_height', dest='aspect_ratio_height', default=1,
                    help='Default height aspect ratio value for image size normalization (default:1)')

args = parser.parse_args()

PICK_CV2_WINDOW_HANDLE = "Image"

class TrainingImage():
    def __init__(self, source_image, filename):
        self._source_image = source_image
        self._path = filename
        self._upper_point = {} 
        self._lower_point = {} 
        self._filename = filename
        self._cropped_image = []
        self._cropped_image_name = "cropped_" + filename

    def crop_image(self, x1, y1, x2, y2, target_aspect_ratio):
        # compute current aspect ratio
        # from the top corner, resize the shorter dimension to fit the target aspect ratio
        # if the resize puts us over the target image size...
        # try from the bottom point
        # if that fails... ?
        self._set_crop_target()
        if target_aspect_ratio != 0:
            current_aspect_ratio = self._crop_height / float(self._crop_width)
            if current_aspect_ratio != target_aspect_ratio:
                if self._crop_width > self._crop_height:
                    target_crop_height = self._crop_width * target_aspect_ratio
                    self._lower_point['y'] = self._upper_point['y'] + int(target_crop_height)
                elif self._crop_width < self._crop_height: 
                    target_crop_width = self._crop_height * target_aspect_ratio
                    self._lower_point['x'] = self._upper_point['x'] + int(target_crop_width)

        self._cropped_image = self.source_image[self._upper_point['y']:self._lower_point['y'], 
                                                self._upper_point['x']:self._lower_point['x']]

    def write_cropped_image(self, destination_directory):
        cv2.imwrite(destination_directory + self._cropped_filename, self._cropped_image) 

    def _set_crop_target(self, x1, y1, x2, y2):
        if y1 > y2:
            self._upper_point['x'] = x1
            self._upper_point['y'] = y1 
            self._lower_point['x'] = x2
            self._lower_point['y'] = y2
        else: 
            self._upper_point['x'] = x2
            self._upper_point['y'] = y2 
            self._lower_point['x'] = x1
            self._lower_point['y'] = y1
        self._crop_width =  abs(x1 - x2)
        self._crop_height = abs(y1 - y2) 

    def show_source_image(self):
        cv2.imshow(PICK_CV2_WINDOW_HANDLE, self._source_image)

    def show_cropped_image(self):
        cv2.imshow(PICK_CV2_WINDOW_HANDLE, self._cropped_image)


def get_filename(index):
    return args.image_path + args.image_prefix + str(index) + args.image_extension

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
    images_metadata = params[0]
    filename = params[1]
    img = params[2]
    if not images_metadata[filename]['clicked']:
        cv2.imshow(PICK_CV2_WINDOW_HANDLE, img)
    if event == cv.CV_EVENT_LBUTTONDOWN:
        print 'Start Mouse Position: ' + str(x) + ', ' + str(y)
        p1 = [x, y]
        images_metadata[filename]['p2'] = []
        images_metadata[filename]['clicked'] = True 
        if p1 != images_metadata[filename]['p1']: 
            images_metadata[filename]['p1'] = p1
    elif event == cv.CV_EVENT_MOUSEMOVE and images_metadata[filename]['clicked']:
        rect_img = img.copy()
        cv2.rectangle(rect_img, (images_metadata[filename]['p1'][0], images_metadata[filename]['p1'][1]),
                     (x, y), (155, 55, 200), 2)
        cv2.imshow(PICK_CV2_WINDOW_HANDLE, rect_img)
    elif event == cv.CV_EVENT_LBUTTONUP:
        print 'End Mouse Position: ' + str(x) + ', ' + str(y)
        p2 = [x, y]
        if p2 != images_metadata[filename]['p2']: 
            images_metadata[filename]['p2'] = p2
            images_metadata[filename]['clicked'] = False 


def mark_images(image_count, images_metadata):
    count = image_count
    while(count < 10000):
        filename = get_filename(count) 
        img = cv2.imread(filename)
        images_metadata[filename] = {}
        images_metadata[filename]['p1'] = []
        images_metadata[filename]['p2'] = []
        images_metadata[filename]['clicked'] = False

        cv2.namedWindow(PICK_CV2_WINDOW_HANDLE)
        cv.SetMouseCallback(PICK_CV2_WINDOW_HANDLE, on_mouse, [images_metadata, filename, img])
        cv2.putText(img, str(count), (1,20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))
        cv2.imshow(PICK_CV2_WINDOW_HANDLE, img)
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

