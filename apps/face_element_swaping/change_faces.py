import cv2
import numpy as np
from shapely.geometry import Point as geometryPoint
from shapely.geometry.polygon import Polygon
from .settings import DEFAULT_CLASSIFIER, PERCENT_OF_NEAREST_NEIGHBOURS
MASK_FILLING_COLOR = np.array([255, 255, 255], dtype=np.uint8)
from math import ceil


class ChangeFaceElement:

    @staticmethod
    def get_bounding_rectangle_of_polygon(polygon):
        polygon_to_adjust = np.float32([polygon])
        bounding_rectangle_of_polygon = cv2.boundingRect(polygon_to_adjust)
        return bounding_rectangle_of_polygon

    @staticmethod
    def get_cropped_polygon(polygon, bounding_rectangle_of_polygon=None):

        if not bounding_rectangle_of_polygon:
            bounding_rectangle_of_polygon = ChangeFaceElement.get_bounding_rectangle_of_polygon(polygon=polygon)

        cropped_polygon = [(point[0] - bounding_rectangle_of_polygon[0],
                            point[1] - bounding_rectangle_of_polygon[1]) for point in polygon]

        return cropped_polygon

    @staticmethod
    def get_warp_mats(mode,
                      src_polygon,
                      dst_polygon,
                      bounding_rectangle_of_src_polygon=None,
                      bounding_rectangle_of_dst_polygon=None):
        # Add cropped points mode
        #raw_polygon, cropped_polygon
        if mode.lower() not in ["raw_polygon", "cropped_polygon"]:
            raise ValueError()

        if mode.lower() == 'raw_polygon':
            cropped_src_polygon = ChangeFaceElement.get_cropped_polygon(polygon=src_polygon)
            cropped_dst_polygon = ChangeFaceElement.get_cropped_polygon(polygon=dst_polygon)
        else:
            cropped_src_polygon = ChangeFaceElement.get_cropped_polygon(polygon=src_polygon,
                                                                        bounding_rectangle_of_polygon=bounding_rectangle_of_src_polygon)
            cropped_dst_polygon = ChangeFaceElement.get_cropped_polygon(polygon=dst_polygon,
                                                                        bounding_rectangle_of_polygon=bounding_rectangle_of_dst_polygon)
        warp_mats = cv2.getPerspectiveTransform(np.float32(cropped_src_polygon),
                                                np.float32(cropped_dst_polygon))
        return warp_mats


    @staticmethod
    def blur_image_colors_via_classifier(classifier,
                                         image_to_blur,
                                         training_image,
                                         rectangle_of_image_to_blur,
                                         polygon_of_image_to_blur):

        training_data = training_image[rectangle_of_image_to_blur[1]:
                                        rectangle_of_image_to_blur[1] + rectangle_of_image_to_blur[3],
                                        rectangle_of_image_to_blur[0]:
                                        rectangle_of_image_to_blur[0] + rectangle_of_image_to_blur[2]]

        shape_of_training_image = training_data.shape
        training_data = np.reshape(training_data, (shape_of_training_image[0] * shape_of_training_image[1],
                                                    shape_of_training_image[2]))
        training_data = np.unique(training_data, axis=0)
        normalized_training_data = (training_data - np.average(training_data, axis=0)) / np.std(training_data, axis=0)

        training_labels = range(training_data.shape[0])
        classifier = classifier(ceil(PERCENT_OF_NEAREST_NEIGHBOURS * training_data.shape[0]))
        classifier.fit(normalized_training_data, training_labels)

        data = image_to_blur[rectangle_of_image_to_blur[1]:
                             rectangle_of_image_to_blur[1] + rectangle_of_image_to_blur[3],
                             rectangle_of_image_to_blur[0]:
                             rectangle_of_image_to_blur[0] + rectangle_of_image_to_blur[2]]

        shape_of_data = data.shape
        data = np.reshape(data, (shape_of_data[0] * shape_of_data[1],
                                 shape_of_data[2]))
        data = (data - np.average(training_data, axis=0)) / np.std(training_data, axis=0)
        labels = classifier.kneighbors(data, return_distance=False)
        #print("labels")
        #print("labels")
        # print("labels")
        #print(labels)
        dst_polygon_object = Polygon(polygon_of_image_to_blur)
        label_idx = 0
        for row_idx in range(rectangle_of_image_to_blur[1],
                             rectangle_of_image_to_blur[1] + rectangle_of_image_to_blur[3]):

            for column_idx in range(rectangle_of_image_to_blur[0],
                                    rectangle_of_image_to_blur[0] + rectangle_of_image_to_blur[2]):

                point = geometryPoint(column_idx, row_idx)
                if dst_polygon_object.contains(point):
                    image_to_blur[row_idx][column_idx] = np.round(np.average(training_data[labels[label_idx]], axis=0)).astype(np.uint8)

                label_idx += 1

        return image_to_blur

    @staticmethod
    def fill_polygon_in_a_rectangle(dst_RGB_array,
                                    dst_polygon,
                                    cropped_dst_RGB_array,
                                    bounding_rectangle_of_dst_polygon):

        dst_polygon_object = Polygon(dst_polygon)
        dst_RGB_array_copy = dst_RGB_array.copy()
        dst_mask = np.zeros_like(dst_RGB_array)

        cropped_dst_RGB_array_row_index = 0
        for row_idx in range(bounding_rectangle_of_dst_polygon[1],
                             bounding_rectangle_of_dst_polygon[1] + bounding_rectangle_of_dst_polygon[3]):
            cropped_dst_RGB_array_column_index = 0
            for column_idx in range(bounding_rectangle_of_dst_polygon[0],
                                    bounding_rectangle_of_dst_polygon[0] + bounding_rectangle_of_dst_polygon[2]):

                point = geometryPoint(column_idx, row_idx)
                if dst_polygon_object.contains(point):
                    dst_RGB_array_copy[row_idx][column_idx] = cropped_dst_RGB_array[cropped_dst_RGB_array_row_index][cropped_dst_RGB_array_column_index]
                    dst_mask[row_idx][column_idx] = MASK_FILLING_COLOR
                cropped_dst_RGB_array_column_index += 1
            cropped_dst_RGB_array_row_index += 1

        center = ((2 * bounding_rectangle_of_dst_polygon[0] + bounding_rectangle_of_dst_polygon[2]) // 2,
                  (2 * bounding_rectangle_of_dst_polygon[1] + bounding_rectangle_of_dst_polygon[3]) // 2)

        mixed_image = cv2.seamlessClone(dst_RGB_array_copy,
                                         dst_RGB_array,
                                         dst_mask,
                                         center,
                                         cv2.NORMAL_CLONE)

        return mixed_image

    @staticmethod
    def changeFaceElement(src_RGB_array,
                          dst_RGB_array,
                          src_polygon,
                          dst_polygon,
                          dst_cut_field=None):

        bounding_rectangle_of_src_polygon = ChangeFaceElement.get_bounding_rectangle_of_polygon(polygon=src_polygon)
        bounding_rectangle_of_dst_polygon = ChangeFaceElement.get_bounding_rectangle_of_polygon(polygon=dst_polygon)

        cropped_src_RGB_array = src_RGB_array[bounding_rectangle_of_src_polygon[1]:
                                              bounding_rectangle_of_src_polygon[1] + bounding_rectangle_of_src_polygon[3],
                                              bounding_rectangle_of_src_polygon[0]:
                                              bounding_rectangle_of_src_polygon[0] + bounding_rectangle_of_src_polygon[2]]

        warp_mats = ChangeFaceElement.get_warp_mats(mode="raw_polygon",
                                                    src_polygon=src_polygon,
                                                    dst_polygon=dst_polygon,
                                                    bounding_rectangle_of_src_polygon=bounding_rectangle_of_src_polygon,
                                                    bounding_rectangle_of_dst_polygon=bounding_rectangle_of_dst_polygon)

        cropped_dst_RGB_array = cv2.warpPerspective(cropped_src_RGB_array,
                                                    warp_mats,
                                                    (bounding_rectangle_of_dst_polygon[2],
                                                     bounding_rectangle_of_dst_polygon[3]),
                                                    None,
                                                    flags=cv2.INTER_LINEAR,
                                                    borderMode=cv2.BORDER_REPLICATE
                                                    )
        if dst_cut_field:
            dst_polygon = dst_cut_field

        mixed_image =  ChangeFaceElement.fill_polygon_in_a_rectangle(dst_RGB_array=dst_RGB_array,
                                                                     dst_polygon=dst_polygon,
                                                                     cropped_dst_RGB_array=cropped_dst_RGB_array,
                                                                     bounding_rectangle_of_dst_polygon=bounding_rectangle_of_dst_polygon)
        return ChangeFaceElement.blur_image_colors_via_classifier(classifier=DEFAULT_CLASSIFIER,
                                                                  image_to_blur=mixed_image,
                                                                  training_image=dst_RGB_array,
                                                                  rectangle_of_image_to_blur=bounding_rectangle_of_dst_polygon,
                                                                  polygon_of_image_to_blur=dst_polygon)

