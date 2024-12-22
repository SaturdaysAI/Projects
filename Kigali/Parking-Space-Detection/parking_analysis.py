import os
import cv2
import time
import requests
from PIL import Image
import streamlit as st
from ultralytics import YOLO
from datetime import datetime
from database import update_daily_summary
from streamlit_js_eval import streamlit_js_eval


@st.cache_resource
def load_parking_model():
    """Load and cache the YOLO model."""
    return YOLO('./model/best.pt')


def process_parking_image(image, notes=""):
    """Process parking image and store results in database."""
    model = load_parking_model()
    results = model(image)
    empty_count, filled_count = 0, 0
    
    # Process detection results
    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            if cls in [0, 3]:  # Empty spots
                empty_count += 1
            elif cls in [1, 2, 4]:  # Filled spots
                filled_count += 1
    
    # Save image to disk
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = f"parking_images/{timestamp}.jpg"
    os.makedirs("parking_images", exist_ok=True)
    if isinstance(image, Image.Image):
        image.save(image_path)
    else:
        cv2.imwrite(image_path, image)
    
    # Calculate metrics
    total_spots = empty_count + filled_count
    efficiency = filled_count / total_spots if total_spots > 0 else 0
    current_hour = datetime.now().hour
    is_peak = 7 <= current_hour <= 19
    peak_hour = f"{current_hour}:00" if is_peak else "Non-peak"
    
    # Calculate revenue (example: $5 per filled spot per hour)
    hourly_rate = 5
    revenue = filled_count * hourly_rate
    
    # Store results in database
    c = st.session_state.cursor
    c.execute('''INSERT INTO parking_analytics 
                 (empty_spots, filled_spots, efficiency, revenue, peak_hour, image_path, notes)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (empty_count, filled_count, efficiency, revenue, peak_hour, image_path, notes))
    
    # Update daily summary
    from database import update_daily_summary
    update_daily_summary(datetime.now().date())
    
    st.session_state.conn.commit()
    
    return empty_count, filled_count, efficiency, revenue, peak_hour


def process_frame(frame, model):
    """Process a single frame and return parking stats."""
    results = model(frame)
    empty_count, filled_count = 0, 0

    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            if cls in [0, 3]:  # Empty spots
                empty_count += 1
            elif cls in [1, 2, 4]:  # Filled spots
                filled_count += 1

    return empty_count, filled_count


def calculate_metrics(empty_count, filled_count):
    """Calculate parking metrics."""
    total_spots = empty_count + filled_count
    efficiency = filled_count / total_spots if total_spots > 0 else 0
    current_hour = datetime.now().hour
    is_peak = 7 <= current_hour <= 19
    peak_hour = f"{current_hour}:00" if is_peak else "Non-peak"

    # Calculate revenue (example: $5 per filled spot per hour)
    hourly_rate = 5
    revenue = filled_count * hourly_rate

    return efficiency, revenue, peak_hour


def store_analysis_result(empty_count, filled_count, efficiency, revenue, peak_hour, frame):
    """Store analysis results in the database."""
    # Save frame to disk
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = f"parking_images/{timestamp}.jpg"
    cv2.imwrite(image_path, frame)

    # Store results in database
    c = st.session_state.cursor
    c.execute('''INSERT INTO parking_analytics 
                 (empty_spots, filled_spots, efficiency, revenue, peak_hour, image_path)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (empty_count, filled_count, efficiency, revenue, peak_hour, image_path))

    # Update daily summary
    update_daily_summary(datetime.now().date())

    st.session_state.conn.commit()


def real_time_analysis(camera_source, analysis_interval=5):
    try:
        cap = cv2.VideoCapture(camera_source)
        if not cap.isOpened():
            raise Exception("Failed to open camera stream")

        """Perform real-time analysis of parking lot camera feed."""
        model = load_parking_model()
        cap = cv2.VideoCapture(camera_source)

        if not cap.isOpened():
            st.error("Error: Could not open camera.")
            return

        last_analysis_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                st.error("Error: Failed to capture frame.")
                break

            # Display the frame
            st.image(frame, channels="BGR", use_column_width=True)

            # Perform analysis at specified intervals
            current_time = time.time()
            if current_time - last_analysis_time >= analysis_interval:
                empty_count, filled_count = process_frame(frame, model)
                efficiency, revenue, peak_hour = calculate_metrics(empty_count, filled_count)

                store_analysis_result(empty_count, filled_count, efficiency, revenue, peak_hour, frame)

                # Display real-time stats
                st.metric("Empty Spots", empty_count)
                st.metric("Filled Spots", filled_count)
                st.metric("Efficiency", f"{efficiency:.2%}")
                st.metric("Estimated Hourly Revenue", f"${revenue:.2f}")
                st.info(f"Current hour: {'Peak' if '7' <= peak_hour <= '19' else 'Off-peak'} ({peak_hour})")

                last_analysis_time = current_time

            # Check for 'q' key press to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("Try using 'http://' instead of 'https://' or add '/video' to the end of the URL.")


def request_camera_permission():
    """Request permission to access the camera."""
    st.warning("This application requires access to your camera for live analysis.")
    permission = st.checkbox("I grant permission to access the camera")
    return permission


def show_camera_access_notification():
    """Show a notification that the camera is about to be accessed."""
    with st.spinner("Preparing to access camera..."):
        st.info("Camera access is about to begin. Please ensure your camera is not in use by another application.")
        st.progress(100)
    st.success("Camera ready for analysis!")


def request_local_camera_permission():
    """Request permission to access the local webcam using browser API."""
    js_code = """
    async function requestCameraPermission() {
        try {
            await navigator.mediaDevices.getUserMedia({ video: true });
            return true;
        } catch (err) {
            console.error("Error accessing camera:", err);
            return false;
        }
    }
    requestCameraPermission();
    """
    return streamlit_js_eval(js_code)


def verify_ip_camera_access(url, username=None, password=None):
    """Verify access to an IP camera."""
    try:
        auth = requests.auth.HTTPBasicAuth(username, password) if username and password else None
        response = requests.get(url, auth=auth, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


def camera_permission_flow(camera_source):
    """Handle the camera permission and notification flow based on the camera source."""
    st.info("Preparing to access camera...")

    try:
        if camera_source == "0" or camera_source.isdigit():
            # Local webcam
            cap = cv2.VideoCapture(int(camera_source))
        else:
            # IP camera
            cap = cv2.VideoCapture(camera_source)

        if not cap.isOpened():
            st.error("Failed to open camera. Please check the camera source and try again.")
            return False

        # Capture a single frame to verify camera access
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture frame from camera. Please check your camera settings.")
            return False

        # Display the captured frame
        st.image(frame, channels="BGR", caption="Camera Feed", use_column_width=True)
        st.success("Camera access granted!")

        # Release the camera
        cap.release()

        return True

    except Exception as e:
        st.error(f"An error occurred while accessing the camera: {str(e)}")
        return False


def run_camera_analysis(camera_source, analysis_interval, camera_feed_placeholder):
    try:
        cap = cv2.VideoCapture(camera_source)
        if not cap.isOpened():
            raise Exception("Failed to open camera stream")

        model = load_parking_model()
        last_analysis_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                st.error("Error: Failed to capture frame.")
                break

            # Display the frame
            camera_feed_placeholder.image(frame, channels="BGR", use_column_width=True)

            # Perform analysis at specified intervals
            current_time = time.time()
            if current_time - last_analysis_time >= analysis_interval:
                empty_count, filled_count = process_frame(frame, model)
                efficiency, revenue, peak_hour = calculate_metrics(empty_count, filled_count)

                store_analysis_result(empty_count, filled_count, efficiency, revenue, peak_hour, frame)

                # Update real-time metrics
                update_realtime_metrics(empty_count, filled_count, efficiency, revenue)

                # Update analytics charts
                update_analytics_charts()

                last_analysis_time = current_time

            # Check if the user wants to stop the analysis
            if st.button("Stop Analysis"):
                break

        cap.release()

    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("If using an IP camera, ensure the URL is correct and the camera is accessible.")