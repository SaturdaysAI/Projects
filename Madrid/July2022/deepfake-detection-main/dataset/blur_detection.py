"""
Detect if a given image is blurred or not using the variation of the Laplacian.
"""
import os
import argparse
from posixpath import join
import cv2

def variance_of_laplacian(image_np_gray):
    """
    Calculate the Laplacian of the image and return the variance of the Laplacian.
    """
    return cv2.Laplacian(image_np_gray, cv2.CV_64F).var()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect if an image is blurred or not.")
    parser.add_argument("image_folder", help="Path to the folder of images to be analyzed.")
    args = parser.parse_args()

    DELETED_FOLDER = "deleted"
    THRESHOLD = 30

    # move the image from img_path to new_path
    images_folder = [path for path in args.image_folder.split("/") if path != ""]
    folder_tag = images_folder[-1]
    deleted_folder_path = os.path.join("/".join(images_folder[:-1]), DELETED_FOLDER)
    if not os.path.exists(deleted_folder_path):
        os.makedirs(deleted_folder_path)
        os.makedirs(os.path.join(deleted_folder_path, "real"))
        os.makedirs(os.path.join(deleted_folder_path, "fake"))

    counter = 0
    for filename in os.listdir(args.image_folder):
        img_path = os.path.join(args.image_folder, filename)
        image = cv2.imread(img_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = variance_of_laplacian(gray)

        if fm < THRESHOLD:
            new_path = os.path.join(deleted_folder_path, folder_tag, filename)
            os.rename(img_path, new_path)
            counter += 1
    
    print(f"Number of images deleted from the {args.image_folder} folder: {counter}")

    # image = cv2.resize(image, (512, 512))
    # blur_status = "blurred" if fm < THRESHOLD else "not blurred"
    # cv2.putText(image, f"{blur_status}: {fm}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
    # window_name = "Image"
    # cv2.imshow(window_name, image)
    # cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
