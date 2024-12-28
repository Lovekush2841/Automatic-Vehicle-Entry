import mysql.connector
import cv2
import os
import pytesseract

# Specify the full path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Database Connection
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Oppoa31#1002',
            database='vehicle_entry'
        )
        if connection.is_connected():
            print("Connected to the database!")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Save Plate to Database
def save_plate_to_db(db_connection, plate_number):
    try:
        cursor = db_connection.cursor()
        query = "INSERT INTO vehicle_logs (plate_number) VALUES (%s)"
        cursor.execute(query, (plate_number,))
        db_connection.commit()
        print(f"Plate number '{plate_number}' saved to database.")
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    finally:
        cursor.close()

# Connect to Database
db_connection = connect_to_database()

if db_connection:
    # Load Cascade
    cascade_path = os.path.join('Automatic-Vehicle-Entry', 'haarcascade_russian_plate_number.xml')
    plate_cascade = cv2.CascadeClassifier(cascade_path)

    # Load Recorded Video
    cap = cv2.VideoCapture(r'Automatic-Vehicle-Entry\parking_video.mp4')  # Replace with the path to your video

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video or cannot read the frame.")
            break

        # Convert to Grayscale and Detect Plates
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        plates = plate_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in plates:
            plate = gray_frame[y:y + h, x:x + w]
            text = pytesseract.image_to_string(plate, config="--psm 8").strip()
            print(f"Detected Plate: {text}")
            
            if text:  # Only save non-empty plate numbers
                save_plate_to_db(db_connection, text)

        # Show Each Processed Frame (Optional)
        cv2.imshow("License Plate Detection", frame)

        # Break on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release Resources
    cap.release()
    cv2.destroyAllWindows()

    # Close Database Connection
    db_connection.close()
    print("Database connection closed.")
else:
    print("Could not establish database connection. Exiting...")
