import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
#.
import socket
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 22222
Message = "0"
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class ColorTrackerApp:
    def __init__(self, root):      
        self.root = root
        self.root.title("Color Tracker")
        self.root.geometry("590x390")
        self.color_var = tk.StringVar()
         # Set the window size
        window_width = 500
        window_height = 330

        # Get the screen dimension
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Find the center position
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        # Set the position of the window to the center of the screen
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Load the image as an attribute to prevent garbage collection
        #self.imageUrl = tk.PhotoImage(file=r"A:\Projects\unity game\tennis photo.png")
        # Load the image as an attribute to prevent garbage collection
        self.imageUrl = tk.PhotoImage(file=r"C:\Users\akash\Downloads\output.png")
        placeImage = tk.Label(self.root, image=self.imageUrl)
        placeImage.place(relheight=1, relwidth=1)
        self.color_var.set("white")  # Default color

        # Create GUI components
        self.create_gui()
    def create_gui(self):
        # Frame for video display
        self.video_frame = ttk.Frame(self.root)
        self.video_frame.pack(padx=5, pady=50)

        # Dropdown for color selection
        color_label = ttk.Label(self.root, text="Select Color:")
        color_label.pack(pady=(0, 10))

        color_options = ["white", "green", "blue", "yellow"]  # Add more colors as needed
        color_dropdown = ttk.Combobox(self.root, values=color_options, textvariable=self.color_var, state="readonly")
        color_dropdown.pack(pady=(0, 70))

        # Start button to begin color tracking
        start_button = ttk.Button(self.root, text="Start Tracking", command=self.start_tracking)
        start_button.pack(pady=(0,20))

    def start_tracking(self):
        color_to_track = self.color_var.get()

        # Call the tracking function with the selected color and video frame
        track_color(color_to_track, self.video_frame)

def track_color(color_name, video_frame):
    color_bounds = {
        "white": ([0, 0, 200], [180, 30, 255]),
        "green": ([40, 100, 100], [80, 255, 255]),
        "blue": ([100, 100, 100], [140, 255, 255]),
        "yellow": ([20, 100, 100], [30, 255, 255]),
    }

    if color_name.lower() not in color_bounds:
        print("Color not supported. Please choose from: white, green, blue, yellow.")
        return

    lower_bound, upper_bound = color_bounds[color_name.lower()]

    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array(lower_bound), np.array(upper_bound))

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            try:
                largest_contour = max(contours, key=cv2.contourArea)
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    # Draw an outline box around the object
                    x, y, w, h = cv2.boundingRect(largest_contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                    # Draw a circle
                    cv2.circle(frame, (cx,cy),5,(0,255,0),-1)
                    
                    print(f"center coordinate:({cx},{cy})")                
                    Message=str(-(cx-320)*(3.7/320))
                    clientSock.sendto(bytes(Message,'utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
            except:
                clientSock.sendto(bytes(Message,'utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
                #print("none exist")
                pass
            
        cv2.imshow("Color Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorTrackerApp(root)
    root.mainloop()
