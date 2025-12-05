import cv2

def capture_leaf_image(filename="leaf_image.jpg", camera_index=0):
    """Captures a single image from the USB camera."""
    cap = cv2.VideoCapture(camera_index) # 0 is usually the default/first camera
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None
    
    # Read a frame
    ret, frame = cap.read()
    
    # Release the camera resource
    cap.release()
    
    if ret:
        # Save the captured frame to a file
        cv2.imwrite(filename, frame)
        print(f"Image captured and saved as {filename}")
        return filename
    else:
        print("Error: Could not capture frame.")
        return None

#