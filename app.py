import cv2
import numpy as np
from rembg import remove

INPUT / OUTPUT 
input_path = "input.mp4"
output_path = "output2.mp4"

# Open video
cap = cv2.VideoCapture(input_path)
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Output video writer
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"Processing {frame_count} frames...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to BGRA for rembg
    frame_bgra = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    # Remove background (keeps person)
    result = remove(frame_bgra)

    # Extract alpha mask
    alpha = result[:, :, 3]
    mask = alpha > 0

    # Create green background
    green_bg = np.zeros_like(frame, dtype=np.uint8)
    green_bg[:] = (0, 255, 0)  # pure green

    # Composite person over green background
    final_frame = np.where(mask[:, :, None], frame, green_bg)

    out.write(final_frame)

cap.release()
out.release()
print("✅ Processing complete. Saved as", output_path)
