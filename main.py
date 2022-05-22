# Copyright 2019 Google LLC
# Test
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo that runs object detection on camera frames using OpenCV.

TEST_DATA=../all_models

Run face detection model:
python3 detect.py \
  --model ${TEST_DATA}/mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite

Run coco model:
python3 detect.py \
  --model ${TEST_DATA}/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite \
  --labels ${TEST_DATA}/coco_labels.txt

"""
import argparse
import cv2
import os
from passengers2 import *
import const
from VideoGet import VideoGet
from VideoShow import VideoShow
import time
#import socket

from pycoral.adapters.common import input_size
from pycoral.adapters.detect import get_objects
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.edgetpu import run_inference

#ClientSocket = socket.socket()
#host = '127.0.0.1'
#port = 1233

area = const.AREA

tracker = Passengers(const.AREA, const.DISTANCE, const.TTL)

def main():
    #store previos values of in, out, and inside
 #   prevEntered = 0
  #  prevExited = 0
   # prevInside = 0
 
    #try:
     #   ClientSocket.connect((host, port))
    #except socket.error as e:
     #   print(str(e))

    is_coco = False

    if is_coco:
        default_model_dir = 'mobilenet_v2'
        default_model = 'mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite'
        default_labels = 'coco_labels.txt'
    else:
        #default_model_dir = 'model_v3_2nh'
        #default_model = 'model.tflite'
        #default_labels = 'model.txt'

        default_model_dir = 'apc_model_ym'
        default_model = 'newModel2022.tflite'
        default_labels = 'model.txt'

    #default_model = 'ssdlite_mobiledet_coco_qat_postprocess_edgetpu.tflite'
    #default_labels = 'coco_labels.txt'

    parser = argparse.ArgumentParser()
    parser.add_argument('--model', help='.tflite model path',
                        default=os.path.join(default_model_dir, default_model))
    parser.add_argument('--labels', help='label file path',
                        default=os.path.join(default_model_dir, default_labels))
    parser.add_argument('--top_k', type=int, default=const.K,
                        help='number of categories with highest score to display')
    parser.add_argument('--camera_idx', type=int, help='Index of which video source to use. ', default=0)
    parser.add_argument('--threshold', type=float, default=const.ACC,
                        help='classifier score threshold')
    args = parser.parse_args()

    print('Loading {} with {} labels.'.format(args.model, args.labels))
    interpreter = make_interpreter(args.model)
    interpreter.allocate_tensors()
    labels = read_label_file(args.labels)
    inference_size = input_size(interpreter)


    video_getter = VideoGet().start()
    video_shower = VideoShow(video_getter.frame).start()


    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break

        frame = video_getter.frame

      #  currentIn = tracker.get_count()[0] 
       # currentOut = tracker.get_count()[1]
        #currentInside = tracker.get_count()[2]
        
      
        height, width, channels = frame.shape
        key = cv2.waitKey(1) & 0xff

        #sleep som funkar
        time.sleep(1/30)
        rotate = False

        if rotate:
            (h, w) = cv2_im.shape[:2]
            w += 50
            #print(h, w)

            center = (w /2, h/2)
            M = cv2.getRotationMatrix2D(center, 90, 1.0)

            frame = cv2.warpAffine(cv2_im, M, (w,h))


        cv2.line(frame, (0, const.AREA[0]), (width, const.AREA[0]), (0, 0, 255))

        cv2.line(frame, (0, const.AREA[1]), (width, const.AREA[1]), (0, 0, 255))

        cv2_im_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2_im_rgb = cv2.resize(cv2_im_rgb, inference_size)
        run_inference(interpreter, cv2_im_rgb.tobytes())
        objs = get_objects(interpreter, args.threshold)[:args.top_k]

        frame = append_objs_to_img(frame, inference_size, objs, labels, const.AREA)
        
        #time.sleep(1/30)

        video_shower.frame = frame

    
        #if in, out, or inside is updated with new value, send taht to the server
       # if prevEntered != currentIn or prevExited != currentOut or prevInside != currentInside:
        #    info =  '{}, {}, {}'.format(currentIn,currentOut,currentInside)
         #   ClientSocket.send(str.encode(info))
        
        #updtae with new values
        #prevEntered = currentIn
        #prevExited =  prevExited
        #prevInside = currentInside

def append_objs_to_img(cv2_im, inference_size, objs, labels, area):
    height, width, channels = cv2_im.shape
    scale_x, scale_y = width / inference_size[0], height / inference_size[1]
    a, b = area[0], area[1]
    detections = []

    for obj in objs:
        bbox = obj.bbox.scale(scale_x, scale_y)
        x0, y0 = int(bbox.xmin), int(bbox.ymin)
        x1, y1 = int(bbox.xmax), int(bbox.ymax)

        dx = int(x1 * 0.6)
        dy = int(y1 * 0.6)

        x0 += dx
        x1 -= dx

        y0 += dy
        y1 -= dy

        if obj.id == 0: #and a < y0 < b:
                #print(obj)
                # percent = int(100 * obj.score)
                # label = '{}% {}'.format(percent, labels.get(obj.id, obj.id))

                 # The center-point of the detected object is calculated by dividing the width and height
                 #of the bounding box of a detected object by two
            center = ((x0 + x1) // 2, (y0 + y1) // 2)
            detections.append([x0, y0, x1, y1])
            cv2_im = cv2.putText(cv2_im, '*', center, cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
            #print(center)
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id, direction = box_id
        rgb = (0, 0, 0)

        if direction > 0 :
            rgb = (0, 255, 0)
        elif direction < 0:
            rgb = (0, 0, 255)

        cv2.putText(cv2_im, str(id), ((x + x1) // 2, (y + y1) // 2 + 20), cv2.FONT_HERSHEY_PLAIN, 2,
                rgb, 2)
        cv2.rectangle(cv2_im, (x, y), (w, h), rgb, 3)
    txt_color = (69, 158, 18)
    cv2.putText(cv2_im, f'Inside:{tracker.get_count()[2]}', (300, 40), cv2.FONT_HERSHEY_PLAIN, 2, txt_color, 2)
    info = f'In:{tracker.get_count()[0]} Out: {tracker.get_count()[1]}'
    cv2.putText(cv2_im, f'{info}', (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, txt_color, 2)

    cv2.putText(cv2_im, f'Area: {const.AREA} Distance: {const.DISTANCE} K: {const.K} ACC: {const.ACC} TTL: {const.TTL}', (20, 80), cv2.FONT_HERSHEY_PLAIN, 1.5, txt_color, 2)
    #print(tracker.get_count())
    return cv2_im


if __name__ == '__main__':
    main()
