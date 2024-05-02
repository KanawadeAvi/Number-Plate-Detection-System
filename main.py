from flask import Flask, request, jsonify
import base64
import cv2
import json
import requests
import time
from collections import OrderedDict
import os



app = Flask(__name__)
CROPPED_IMAGES_FOLDER = os.path.join(os.getcwd(), 'cropped_images')  # Define the folder for cropped images

def process_image(base64_string):
    # Convert base64 string to image
    image_bytes = base64.b64decode(base64_string)
    image_array = bytearray(image_bytes)
    path = 'temp_image.jpg'
    with open(path, 'wb') as f:
        f.write(image_array)

    # Perform number plate recognition
    result = []
    with open(path, 'rb') as fp:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            files=dict(upload=fp),
            data=dict(regions='fr'),
            headers={'Authorization': 'Token ' + '46569c6bbf83ec3257068d20a74113e420598687'}
        )
    result.append(response.json(object_pairs_hook=OrderedDict))
    time.sleep(1)
    im = cv2.imread(path)

    # Process the result
    resp_dict = json.loads(json.dumps(result, indent=2))
    num = resp_dict[0]['results'][0]['plate'].upper()
    boxs = resp_dict[0]['results'][0]['box']
    xmins, ymins, ymaxs, xmaxs = boxs['xmin'], boxs['ymin'], boxs['ymax'], boxs['xmax']

    # Draw rectangle and label on the image
    cv2.rectangle(im, (xmins, ymins), (xmaxs, ymaxs), (255, 0, 0), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(im, num, (xmins, ymins - 10), font, 1, (255, 0, 0), 2, cv2.LINE_AA)

    # Save the cropped image in the specific folder
    try:
        if not os.path.exists(CROPPED_IMAGES_FOLDER):
            os.makedirs(CROPPED_IMAGES_FOLDER)
    except Exception as e:
        print(f"Error creating directory: {e}")

    cropped_image_path = os.path.join(CROPPED_IMAGES_FOLDER, f'{num}.jpg')
    cropped_image = im[ymins:ymaxs, xmins:xmaxs]
    cv2.imwrite(cropped_image_path, cropped_image)

    # Cleanup
    cv2.imwrite('output_image.jpg', im)
    cv2.destroyAllWindows()

    return num


@app.route('/detect_plate', methods=['POST'])
def detect_plate():
    data = request.json
    base64_string = data.get('image', None)
    if base64_string is None:
        return jsonify({'error': 'No image provided'}), 400

    plate_number = process_image(base64_string)
    return jsonify({'plate_number': plate_number})

if __name__ == '__main__':
    app.run(debug=True)
