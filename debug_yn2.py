#!/usr/bin/env python
"""
Classifier is an image classifier specialization of Net.
"""
import numpy as np
# The caffe module needs to be on the Python path;
#  we'll add it here explicitly.
import sys
caffe_root = '/mnt/lustre/yangkunlin/sensenet_disp/'
myself = '/mnt/lustre/yangkunlin/kaggle_camera/SE-ResNeXt-50/'
sys.path.insert(0, caffe_root + 'core/python')
import caffe
caffe.mpi_init()
import os
import csv
import cv2
from multiprocessing.dummy import Pool
pool = Pool(30)

# Multi crop testing. This function can get (crop_num**2*2) crops.
def _oversample(images, crop_dims, crops_num):

    im_shape = np.array(images[0].shape)
    crop_dims = np.array(crop_dims)
    im_center = im_shape[:2] / 2.0

    # Make crop coordinates

    delta_h = int(im_shape[0]-crop_dims[0])/crops_num
    delta_w = int(im_shape[1]-crop_dims[1])/crops_num
    h_indices = [x*delta_h for x in range(int(crops_num))]
    w_indices = [x*delta_w for x in range(int(crops_num))]

    crops_ix = np.empty((crops_num**2, 4), dtype=int)
    curr = 0
    for i in h_indices:
        for j in w_indices:
            crops_ix[curr] = (i, j, i + crop_dims[0], j + crop_dims[1])
            curr += 1
    
    crops_ix = np.tile(crops_ix, (2, 1))

    # Extract crops
    crops = np.empty((crops_num**2*2 * len(images), crop_dims[0], crop_dims[1],
                      im_shape[-1]), dtype=np.float32)
    ix = 0
    for im in images:
        for crop in crops_ix:
            crops[ix] = im[crop[0]:crop[2], crop[1]:crop[3], :]
            ix += 1
        crops[ix- crops_num**2:ix] = crops[ix- crops_num**2:ix, :, ::-1, :]  # flip for mirrors
    return crops


class Classifier(caffe.Net):
    """
    Classifier extends Net for image class prediction
    by scaling, center cropping, or oversampling.
    Parameters
    ----------
    image_dims : Image_dims is the real-dims of an image, just useful when doing crop.
    mean, input_scale, raw_scale, channel_swap: params for
        preprocessing options.
    """
    def __init__(self, model_file, pretrained_file, image_dims=None,
            mean=None, raw_scale=None,
            channel_swap=None, input_scale=None):
        caffe.Net.__init__(self, model_file, pretrained_file, caffe.TEST)

        # configure pre-processing
        in_ = self.inputs[0]
        self.transformer = caffe.io.Transformer(
                {in_: self.blobs[in_].data.shape})
        self.transformer.set_transpose(in_, (2, 0, 1))
        if mean is not None:
            self.transformer.set_mean(in_, mean)
        if input_scale is not None:
            self.transformer.set_input_scale(in_, input_scale)
        if raw_scale is not None:
            self.transformer.set_raw_scale(in_, raw_scale)
        if channel_swap is not None:
            self.transformer.set_channel_swap(in_, channel_swap)

        self.crop_dims = np.array(self.blobs[in_].data.shape[2:]) # crop_dims are the input-dims of the Net, 
        # Image_dims is the real-dims of an image, just useful when doing crop.
        if not image_dims:
            image_dims = self.crop_dims
        self.image_dims = image_dims


    def predict(self, inputs, oversample=True):
        """
        Predict classification probabilities of inputs.
        Parameters
        ----------
        inputs : iterable of (H x W x K) input ndarrays.
        oversample : boolean
            average predictions across center, corners, and mirrors
            when True (default). Center-only prediction when False.
        Returns
        -------
        predictions: (N x C) ndarray of class probabilities for N images and C
            classes.
        """
        # Scale to standardize input dimensions.
        input_ = np.zeros((len(inputs),
            self.image_dims[0],
            self.image_dims[1],
            inputs[0].shape[2]),
            dtype=np.float32)
        for ix, in_ in enumerate(inputs):
            if(in_.shape[0]!=self.image_dims[0] or in_.shape[1]!=self.image_dims[1]):
                input_[ix] = caffe.io.resize_image(in_, self.image_dims)
            else:
                input_[ix] = in_

        if oversample:
            # Generate center, corner, and mirrored crops.
            print "oversampling..."
            input_ = _oversample(input_, self.crop_dims,8) #########
        else:
            # Take center crop.
            center = np.array(self.image_dims) / 2.0
            crop = np.tile(center, (1, 2))[0] + np.concatenate([
                -self.crop_dims / 2.0,
                self.crop_dims / 2.0
                ])
            crop = crop.astype(int)
            input_ = input_[:, crop[0]:crop[2], crop[1]:crop[3], :]

        # Classify
        caffe_in = np.zeros(np.array(input_.shape)[[0, 3, 1, 2]],
                dtype=np.float32)
        print "data preprocessing..."
        for ix, in_ in enumerate(input_):
            caffe_in[ix] = self.transformer.preprocess(self.inputs[0], in_)
        print "net forward..."
        out = self.forward_all(**{self.inputs[0]: caffe_in})
        prediction = out[self.outputs[0]]

        # For oversampling, average predictions across crops.

        print "do mean output"
        if oversample:
            prediction = prediction.reshape((len(prediction) / 128, 128, -1))
            prediction = prediction.mean(1)
        return prediction




def input_worker(file_name):
    img = cv2.imread(file_name)
    return img


def make_inputs(image_dir, textfile):
    file_ = open(textfile)
    lines = file_.readlines()
    file_names = []
    num = 0
    for line in lines:
        image = line.split(' ')[0]
        file_names.append(image_dir + image)
        if num==0:
            print(image_dir)
            print(image_dir+image)
        # print("num is: {} ".format(num))
        num += 1
        # img = caffe.io.load_image(os.path.join(image_dir, image))
    res = pool.map(input_worker,file_names)
    return res


def doClassify(model_def, model_weights, test_dir, test_txt):
    caffe.set_mode_gpu()
    model_def = model_def
    model_weights = model_weights
    predictor = Classifier(model_def, model_weights, image_dims=(512, 512), mean=np.array([103.939, 116.779, 123.68], dtype='float64'))
    print "make input..."
    inputs = make_inputs(test_dir, test_txt)
    pred = predictor.predict(inputs, oversample=True)
    # print(pred)
    np.save('/mnt/lustre/yangkunlin/kaggle_camera/SE-ResNeXt-50/rst/prob_test128.npy', pred)
    caffe.mpi_fin()


# model_def = myself+'SE-ResNeXt-50_multi.prototxt'
# model_weights = '/mnt/lustre/yangkunlin/kaggle_camera/SE-ResNeXt-50/model_aug2-1/SE-ResNeXt-50_iter_200000.caffemodel'
# print(model_weights)
# test_dir = '/mnt/lustre/yangkunlin/kaggle_camera/data/test/'
# test_txt = '/mnt/lustre/yangkunlin/kaggle_camera/data/test0.txt'
# doClassify(model_def, model_weights, test_dir, test_txt)




def main():
    model_def = myself + 'SE-ResNeXt-50_multi.prototxt'
    model_weights = '/mnt/lustre/yangkunlin/kaggle_camera/SE-ResNeXt-50/model_aug2-1/SE-ResNeXt-50_iter_200000.caffemodel'
    test_dir = '/mnt/lustre/yangkunlin/kaggle_camera/data/test/'
    caffe.set_mode_gpu()
    model_def = model_def
    model_weights = model_weights
    predictor = Classifier(model_def, model_weights, image_dims=(512, 512),
                           mean=np.array([103.939, 116.779, 123.68], dtype='float64'))
    print("model is {}".format(model_weights))
    for i in xrange(53):
        print("processing {}".format(i))
        test_txt = '/mnt/lustre/yangkunlin/kaggle_camera/SE-ResNeXt-50/TestList/'+'testL{}.txt'.format(i)
        # doClassify(model_def, model_weights, test_dir, test_txt, i)
        print "make input..."
        inputs = make_inputs(test_dir, test_txt)
        # print("inputs type is: {}".format(type(inputs[0])))
        pred = predictor.predict(inputs, oversample=True)
        # print(pred)
        np.save('/mnt/lustre/yangkunlin/kaggle_camera/SE-ResNeXt-50/test_prob2/prob_test_{}.npy'.format(i), pred)
    caffe.mpi_fin()

if __name__ == '__main__':
    main()
