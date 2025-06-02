import cv2
import numpy as np
import math

img_path = '/Users/krishnanujam/Desktop/captured_image.jpeg'
output_path = '/Users/krishnanujam/Desktop/undistorted.jpeg'

distorted_img = cv2.imread(img_path)
if distorted_img is None:
    raise FileNotFoundError(f"Image not found at {img_path}")

K = np.array([[3500, 0, distorted_img.shape[1] / 2],
              [0, 3500, distorted_img.shape[0] / 2],
              [0, 0, 1]], dtype=np.float32)
D = np.array([-0.7, 0.7, 0, 0], dtype=np.float32)

h, w = distorted_img.shape[:2]
new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(K, D, (w, h), np.eye(3), balance=0.0)
map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), new_K, (w, h), cv2.CV_16SC2)
undistorted_img = cv2.remap(distorted_img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

cv2.imwrite(output_path, undistorted_img)
print(f"Undistorted image saved at {output_path}")

image = cv2.imread(output_path)
pointCoordinates1 = []
pointCoordinates2 = []
scale_length = None
scale_pixels = None

def click_points(event, x, y, flags, param):
    global pointCoordinates1, pointCoordinates2, scale_length

    if event == cv2.EVENT_LBUTTONDOWN:
        coordinate = (x, y)
        if not scale_length:
            if len(pointCoordinates1) < 2:
                pointCoordinates1.append(coordinate)
            else:
                pointCoordinates1 = [coordinate]
        else:
            if len(pointCoordinates2) < 2:
                pointCoordinates2.append(coordinate)
            else:
                pointCoordinates2 = [coordinate]

        cv2.circle(image, (x, y), 4, (255, 255, 255), 4)
        cv2.imshow("Image", image)

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def set_scale_length():
    global scale_length, scale_pixels
    if len(pointCoordinates1) == 2:
        x1, y1 = pointCoordinates1[0]
        x2, y2 = pointCoordinates1[1]
        scale_pixels = calculate_distance(x1, y1, x2, y2)
        scale_length = float(input("Enter the actual length (in cm) of the selected scale: "))

def calculate_length():
    global scale_length, scale_pixels
    if len(pointCoordinates2) == 2:
        x1, y1 = pointCoordinates2[0]
        x2, y2 = pointCoordinates2[1]
        pixels = calculate_distance(x1, y1, x2, y2)
        length = (pixels * scale_length) / scale_pixels
        print(f"Measured Length: {length:.2f} cm")

cv2.imshow("Image", image)
cv2.setMouseCallback("Image", click_points)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("s"):
        set_scale_length()
    elif key == ord("m"):
        calculate_length()
    elif key == ord("q"):
        break

cv2.destroyAllWindows()
