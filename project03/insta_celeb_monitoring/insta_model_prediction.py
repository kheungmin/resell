import pandas as pd
import numpy as np
import time
import pymongo
import os

import tensorflow as tf
import tensorflow_hub as hub
from keras.models import load_model

import matplotlib.pyplot as plt
import tempfile
from urllib.request import urlopen
from six import BytesIO

import cv2
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps


# 이미지 보여 주기
def display_image(image):
    fig = plt.figure(figsize=(20, 15))
    plt.grid(False)
    plt.imshow(image)


# url 
def download_and_resize_image(url,display=False):
    _, filename = tempfile.mkstemp(suffix=".jpg")
    response = urlopen(url)
    image_data = response.read()
    image_data = BytesIO(image_data)
    pil_image = Image.open(image_data)
    pil_image = ImageOps.fit(pil_image, (pil_image.size[0], pil_image.size[1]), Image.ANTIALIAS)
    pil_image_rgb = pil_image.convert("RGB")
    pil_image_rgb.save(filename, format="JPEG", quality=90)
    print("Image downloaded to %s." % filename)
    if display:
        display_image(pil_image)
    return filename


def draw_bounding_box_on_image(image, ymin, xmin, ymax, xmax, color, font, thickness=4, display_str_list=()):
    """Adds a bounding box to an image."""
    draw = ImageDraw.Draw(image)
    im_width, im_height = image.size
    (left, right, top, bottom) = (xmin * im_width, xmax * im_width, ymin * im_height, ymax * im_height)
    draw.line([(left, top), (left, bottom), (right, bottom), (right, top), (left, top)], width=thickness, fill=color)

    # If the total height of the display strings added to the top of the bounding
    # box exceeds the top of the image, stack the strings below the bounding box
    # instead of above.
    display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
    # Each display_str has a top and bottom margin of 0.05x.
    total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

    if top > total_display_str_height:
        text_bottom = top
    else:
        text_bottom = top + total_display_str_height
    # Reverse list and print from bottom to top.

    
    for display_str in display_str_list[::-1]:
        text_width, text_height = font.getsize(display_str)
        margin = np.ceil(0.05 * text_height)
        draw.rectangle([(left, text_bottom - text_height - 2 * margin),
                        (left + text_width, text_bottom)],
                        fill=color)
        draw.text((left + margin, text_bottom - text_height - margin),
              display_str,
              fill="black",
              font=font)
        text_bottom -= text_height - 2 * margin


def draw_boxes(image, boxes, class_names, scores, max_boxes=10, min_score=0.1):
    """Overlay labeled boxes on an image with formatted scores and label names."""
    colors = list(ImageColor.colormap.values())

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf", 25)
    except IOError:
        print("Font not found, using default font.")
        font = ImageFont.load_default()

    for i in range(min(boxes.shape[0], max_boxes)):
        if scores[i] >= min_score:
            ymin, xmin, ymax, xmax = tuple(boxes[i])
            display_str = "{}: {}%".format(class_names[i].decode("ascii"), int(100 * scores[i]))
            color = colors[hash(class_names[i]) % len(colors)]
            image_pil = Image.fromarray(np.uint8(image)).convert("RGB")
            draw_bounding_box_on_image(
                image_pil,
                ymin,
                xmin,
                ymax,
                xmax,
                color,
                font,
                display_str_list=[display_str]
            )
            np.copyto(image, np.array(image_pil))
    return image


def load_img(path):
    img = tf.io.read_file(path)
    img = tf.image.decode_jpeg(img, channels=3)
    return img


def run_detector(detector, path):
    
    img = load_img(path)

    converted_img  = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
    start_time = time.time()
    result = detector(converted_img)
    end_time = time.time()
    
    global result1

    result1 = {key:value.numpy() for key,value in result.items()}
    
    

    print("Found %d objects." % len(result["detection_scores"]))
    print("Inference time: ", end_time-start_time)
    print(converted_img.shape)

    image_with_boxes = draw_boxes(
    img.numpy(), result1["detection_boxes"],
    result1["detection_class_entities"], result1["detection_scores"])
    
    
# 인스타그램 사진 불러오고 저장
def insta_picture(image_url, save_path, detector):
    downloaded_image_path = download_and_resize_image(image_url, False)
    
    run_detector(detector, downloaded_image_path)
    
    result_final = pd.DataFrame(result1["detection_boxes"])
    result_final.columns = ["ymin", "xmin", "ymax", "xmax"]
    img_color = Image.open(downloaded_image_path)
    result_final["xmin"] = round(result_final["xmin"]*img_color.size[0])
    result_final["xmax"] = round(result_final["xmax"]*img_color.size[0])
    result_final["ymin"] = round(result_final["ymin"]*img_color.size[1])
    result_final["ymax"] = round(result_final["ymax"]*img_color.size[1])
    result_final_array = result_final.values
    

    empty_df = pd.DataFrame(columns = ["ymin", "xmin", "ymax", "xmax", "score"])

    for i in range(min(result1["detection_boxes"].shape[0], 10)):
        if result1["detection_class_entities"][i] == b'Footwear':
            if result1["detection_scores"][i] > 0.1:
                ymin, xmin, ymax, xmax = tuple(result_final_array[i])
                empty_df.loc[i] = [ymin, xmin, ymax, xmax, result1["detection_scores"][i]]
            
    empty_df = empty_df.sort_values(by="score", ascending=False).reset_index(drop=True)
    
    empty_df = empty_df.astype({'ymin':'int'})
    empty_df = empty_df.astype({'xmin':'int'})
    empty_df = empty_df.astype({'ymax':'int'})
    empty_df = empty_df.astype({'xmax':'int'})
    
    try:
        xmin = empty_df.loc[0, "xmin"]
        ymin = empty_df.loc[0, "ymin"]
        xmax = empty_df.loc[0, "xmax"]
        ymax = empty_df.loc[0, "ymax"]
        
        croppedImage=img_color.crop((xmin, ymin, xmax, ymax))
        croppedImage.save(f"{save_path}.png", 'png')
        
    except (ValueError, KeyError):
        pass
    

# 이미지 조정
def image_resize(save_path):
    im = Image.open(f'{save_path}.png')
    im = im.resize((100, 100))
    im.save(f'{save_path}.png')
    

def model_predict(save_path):
    model = load_model('objection_detection_100_12.h5')
    image = cv2.imread(f"{save_path}.png")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    test_data = image / 255.0
    pred = model.predict(test_data[np.newaxis, ...])
    product_lst = [
        "Jordan 1 Retro High OG Black Mocha",
        "Jordan 1 Retro High OG University Blue",
        "Jordan 1 x Travis Scott x Fragment Retro Low OG SP Military Blue",
        "other"]

    return product_lst[np.argmax(pred)] 


if __name__ == '__main__':
    cur_dir = '/home/ubuntu/airflow/dags/resell/insta_celeb_monitoring'

    user = 'team04'
    pw = '1111'
    host = 'ec2-54-95-8-243.ap-northeast-1.compute.amazonaws.com'
    client = pymongo.MongoClient(f'mongodb://{user}:{pw}@{host}:27017/')
    db = client.resell
    
    df = pd.DataFrame(db.insta.find({'new': 1}, {'_id': 0, 'user': 1, 'img_url': 1}))
    if len(df) > 0:
        module_handle = "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"
        detector = hub.load(module_handle).signatures['default']
        
        with open(f'{cur_dir}/message.txt', 'w', encoding='utf-8') as f:
            for idx, row in df.iterrows():
                try:
                    insta_picture(row['img_url'], f'{cur_dir}/{idx}', detector)
                    image_resize(f'{cur_dir}/{idx}')
                    product = model_predict(f'{cur_dir}/{idx}')
                    
                    os.remove(f'{cur_dir}/{idx}.png')
                    if product != 'other':
                        f.write(f'{row["user"]}님이 {product}를 착용하였습니다.\n')
                except Exception as e:
                    print(e)
                finally:
                    db.insta.update_one({'img_url': row['img_url']}, {'$set': {'new': 0}})
    