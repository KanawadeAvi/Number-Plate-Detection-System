from __future__ import absolute_import, division, print_function

import json
import time
from collections import OrderedDict
import cv2
import requests

def main():
    path = '10.jpg'
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

    resp_dict = json.loads(json.dumps(result, indent=2))
    num = resp_dict[0]['results'][0]['plate']
    boxs = resp_dict[0]['results'][0]['box']
    xmins, ymins, ymaxs, xmaxs = boxs['xmin'], boxs['ymin'], boxs['ymax'], boxs['xmax']
   
    cv2.rectangle(im, (xmins, ymins), (xmaxs, ymaxs), (255, 0, 0), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(im, num, (xmins, ymins - 10), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
    
    print(f"The detected car number is: {num}")

    cv2.imshow("Number Plate Detection", im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
