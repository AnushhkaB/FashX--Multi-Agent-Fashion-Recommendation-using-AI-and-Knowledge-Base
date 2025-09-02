import os
import csv
import numpy as np
from tqdm import tqdm
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model

# --- Config ---
IMAGE_DIR = 'path/to/image/folder'  # Folder containing images
OUTPUT_CSV = 'image_embedding.csv'  # Output CSV path
IMAGE_SIZE = (224, 224)             # Input size for ResNet50

# --- Load Model ---
base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
model = Model(inputs=base_model.input, outputs=base_model.output)

# --- Get image files ---
image_files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.jpg', '.png'))]

# --- Write CSV ---
with open(OUTPUT_CSV, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['article_id', 'image_embedding'])

    for img_file in tqdm(image_files, desc='Processing images'):
        article_id = os.path.splitext(img_file)[0]  # Use filename (without extension) as article_id
        img_path = os.path.join(IMAGE_DIR, img_file)

        try:
            img = image.load_img(img_path, target_size=IMAGE_SIZE)
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            embedding = model.predict(x)[0]
            embedding_str = "[" + ",".join(map(str, embedding.tolist())) + "]"

            writer.writerow([article_id, embedding_str])

        except Exception as e:
            print(f"Error processing {img_file}: {e}")

