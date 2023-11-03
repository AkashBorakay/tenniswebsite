# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 10:22:10 2023

@author: SybilleDarbin
"""

import cv2 
from flask_restful import Resource

class QrScanner(Resource):
    
    def get(self):
                
        delay = 1
        window_name = 'Scan QR Code'
        qcd = cv2.QRCodeDetector()
        cap = cv2.VideoCapture(0)
        HIGH_VALUE = 10000
        WIDTH = HIGH_VALUE
        HEIGHT = HIGH_VALUE
    
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        while True:
            ret, frame = cap.read()
            # frame = cv2.resize(frame, (width, height))
            if ret:
                ret_qr, decoded_info, points, _ = qcd.detectAndDecodeMulti(frame)
                if ret_qr:
                    for s, p in zip(decoded_info, points):
                        if s:
                            color = (0, 255, 0)
                            cv2.destroyWindow(window_name)
                            return {"message" : 1, "DecryptQRCode" : s}
                        else:
                            color = (0, 0, 255)
                        frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)
                cv2.imshow(window_name, frame)

                if cv2.waitKey(delay) & 0xFF == ord('q'):
                    break
        cv2.destroyWindow(window_name)
        return {"message" : 0}
                
                
