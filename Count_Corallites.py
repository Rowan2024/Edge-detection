import os
import cv2
import matplotlib.pyplot as plt
import pandas as pd


# Define the folder with corallite predictions
folder_path = r'C:\Users\rowan\OneDrive - University of Bristol\Coral samples\LB_0048\cropped_human'

# Create lists to store vertical distances and dot counts
vertical_distances = []
dot_counts = []

# Conversion factor to mm
distance_per_image_mm = 0.076927  # <---- Adjust according to sample (voxel size)

# Total area of the image in mm^2
total_area_mm2 = 23.00 * 21.39

# List all files in the folder
files = sorted(os.listdir(folder_path))

# Run through every file in the prediction folder
for idx, file in enumerate(files):
    # Check the file is the same format as prediction files
    if file.endswith('.png'):

        vertical_distance_mm = idx * distance_per_image_mm # Convert images to vertical distance
        vertical_distances.append(vertical_distance_mm) # Append vertical distance to list
        image_path = os.path.join(folder_path, file) # Construct the path to the image

        # Read image and convert to greyscale
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Separate white dots from black background and identify contours
        _, thresholded = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter out rogue pixels: a massive Porites spp. corallite should be around 1mm^2
        min_area = 0 # <---- adjust to stop rogue pixels being counted as a corallite
        max_area = 100 # <---- adjust to stop large objects that aren't corallites being predicted
        filtered_contours = [cnt for cnt in contours if min_area < cv2.contourArea(cnt) < max_area]

        # Count white dots post filtering and append to list
        num_white_dots = len(filtered_contours)
        dot_counts.append(num_white_dots)

# Create a DataFrame to organize the data for output
data = {'Vertical Distance (mm)': vertical_distances,
        'Corallite count': dot_counts}
df = pd.DataFrame(data)

# Plot the data
plt.figure(figsize=(6, 10))  # Adjust the figure size to be more vertical
plt.plot(dot_counts, vertical_distances, marker='none', linestyle='-')
plt.title('Corallite prediction count vs. Vertical distance', fontname='Arial', fontsize=16)
plt.xlabel('Corallite count', fontname='Arial', fontsize=14)
plt.ylabel('Vertical distance (mm)', fontname='Arial', fontsize=14)
plt.gca().invert_yaxis()  # Invert the y-axis
plt.grid(False)
plt.show()

# Output data to an Excel file
output_folder = r'C:\Users\rowan\OneDrive - University of Bristol\Documents'
df.to_excel("Corallite_count.xlsx", index=False, columns=['Vertical Distance (mm)', 'Corallite count'])
print(f"Data saved to '{output_folder}'")
