#importing all the necessary libraries
from scipy.spatial import distance as dist
from imutils import perspective, contours
import numpy as np
import imutils
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
matplotlib.rcParams['figure.figsize'] = (10, 6)
import cv2 as cv
import builtins
zip = builtins.zip
import matplotlib.pyplot as plt
from tabulate import tabulate
from PIL import Image
import base64
import boto3
import os
import joblib
import sklearn
from imutils.perspective import order_points
from xgboost import XGBRegressor
import xgboost
import xgboost as xgb


def extract_rgb_values(image):
    # Convert to grayscale
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    _, thresh = cv.threshold(gray, 200, 255, cv.THRESH_BINARY)
    kernel = np.ones((3, 3))
    thresh = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=2)

    # Find contours
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    min_area = 10000
    valid_contours = [cnt for cnt in contours if cv.contourArea(cnt) > min_area]

    mask = np.zeros_like(image, dtype=np.uint8)

    for cnt in valid_contours:
        cv.drawContours(mask, [cnt], -1, (255, 255, 255), thickness=cv.FILLED)

    # Erode the mask to shrink it slightly
    erosion_kernel = np.ones((2, 2), np.uint8)
    mask = cv.erode(mask, erosion_kernel, iterations=1)

    # Apply the mask to the original image
    result = cv.bitwise_and(image, mask)

    # Get valid pixels for RGB extraction
    valid_mask = mask[:, :, 0] > 0
    rgb_values = image[valid_mask]

    if len(rgb_values) == 0:
        return [0, 0, 0]  # Handle case with no valid RGB values

    average_rgb = np.mean(rgb_values, axis=0)
    return average_rgb

def linear_interpolation(wi_list, ref_wi_list, wi_target):
    for i in range(len(wi_list) - 1):
        if wi_list[i] <= wi_target <= wi_list[i + 1]:
            wi1, wi2 = wi_list[i], wi_list[i + 1]
            x1, x2 = ref_wi_list[i], ref_wi_list[i + 1]
            return x1 + ((x2 - x1) / (wi2 - wi1)) * (wi_target - wi1)
    return None  # Return None if target WI is out of bounds

   
def whiteness_analysis(contents, id):            
    nparr = np.fromstring(contents, np.uint8)
    im = cv.imdecode(nparr, cv.IMREAD_COLOR)
   
    if im is None:
        raise ValueError("Image could not be loaded.")

    im_pil = Image.fromarray(cv.cvtColor(im, cv.COLOR_BGR2RGB))
    image_cropped = im_pil.crop(box=(640, 50, 3950, 3350))
    image = cv.cvtColor(np.array(image_cropped), cv.COLOR_RGB2BGR)

    bowl_region = im_pil.crop((1500, 0, 3500, 1800))
    bowl_rgb = extract_rgb_values(cv.cvtColor(np.array(bowl_region), cv.COLOR_RGB2BGR))
    WI_correct = 100 - np.sqrt((255 - bowl_rgb[0])**2 + (255 - bowl_rgb[1])**2 + (255 - bowl_rgb[2])**2)
    print("whitness_correct = ", WI_correct)
    
    bucket_name = "agsurebucket"
    model_folder = "models"

    model_filename = f"{id}.csv"
    local_model_path = os.path.join("/tmp", model_filename)

    if not os.path.exists(local_model_path):
            try:
                s3 = boto3.client('s3')
                s3_key = f"{model_folder}/{model_filename}"
                print(f"Downloading model from S3: {bucket_name}/{model_folder}/{model_filename}")
                s3.download_file(bucket_name, s3_key, local_model_path)
              
            except Exception as e:
                raise ValueError(f"Failed to download model from S3: {str(e)}")

    try:
            df = pd.read_csv(local_model_path)
            if 'REF_WI' not in df.columns or 'WI' not in df.columns:
                raise ValueError("CSV file does not contain required columns: 'REF_WI' or 'WI'")
            df_sorted = df.sort_values(by='REF_WI').reset_index(drop=True)
            wi = df_sorted['WI'].values
            ref_wi = df_sorted['REF_WI'].values

    except Exception as e:
        raise ValueError(f"Error loading CSV file: {str(e)}")

   
   try:
       y_pred = linear_interpolation(wi, ref_wi, WI_correct)
        temp_var = y_pred
        if temp_var <  min(ref_wi):             #:18.00:
            temp_var = 19.0
        elif temp_var >= max(ref_wi):           #:34.50:
            temp_var = 34.5
        result = {"whiteness_cat":temp_var}  # Extract the prediction result
        return result  # Return the result if necessary

    except Exception as e:
        raise ValueError(f"Error in prediction:{str(e)}")

    

