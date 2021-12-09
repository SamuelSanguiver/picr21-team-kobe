#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import image_processor
from color import Color


class ProcessFrames:
    def __init__(self, camera, target=Color.BLUE):
        self.processor = image_processor.ImageProcessor(camera.cam, debug=True)
        self.target = target

    def set_target(self, target):
        self.target = target

    def process_frame(self, align_frame=False):
        processed = self.processor.process_frame(aligned_depth=align_frame)
        ball_array = processed.balls
        x = None
        y = None
        basket = None
        basket_x_center = None
        basket_y_center = None
        basket_distance = None
        out_of_field = False

        out_of_field = processed.out_of_field

        if self.target == Color.BLUE:
            basket = processed.basket_b
        else:
            basket = processed.basket_m

        if basket.exists:
            basket_x_center = basket.x
            basket_y_center = basket.y
            basket_distance = basket.distance

        floor_area = np.count_nonzero(processed.fragmented == int(Color.ORANGE))

        if floor_area is None:
            floor_area = 0

        if len(ball_array) > 0:
            x = ball_array[0].x
            y = ball_array[0].y

        basket_size = basket.size

        cv2.imshow("Debug", processed.debug_frame)

        return (len(ball_array),
                y,
                x,
                basket_x_center,
                basket_y_center,
                basket_distance,
                floor_area,
                out_of_field,
                basket_size)
