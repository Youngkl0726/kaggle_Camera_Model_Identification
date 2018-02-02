#!/usr/bin/env python
"""
Classifier is an image classifier specialization of Net.
"""
import numpy as np
# The caffe module needs to be on the Python path;
#  we'll add it here explicitly.
import sys
caffe_root = ''
myself = ''
sys.path.insert(0, caffe_root + 'core/python')
import caffe
caffe.mpi_init()
import os
import csv
import cv2



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
            input_ = caffe.io.oversample(input_, self.crop_dims)
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
        for ix, in_ in enumerate(input_):
            caffe_in[ix] = self.transformer.preprocess(self.inputs[0], in_)
        out = self.forward_all(**{self.inputs[0]: caffe_in})
        prediction = out[self.outputs[0]]

        # For oversampling, average predictions across crops.
        if oversample:
            prediction = prediction.reshape((len(prediction) / 10, 10, -1))
            prediction = prediction.mean(1)
        return prediction




def make_inputs(image_dir, textfile):
    file_ = open(textfile)
    lines = file_.readlines()
    inputs = []
    for line in lines:
        image = line.split(' ')[0]
        # print image
        # print os.path.join(image_dir, image)
        img = cv2.imread(os.path.join(image_dir, image),-1)
        inputs.append(img)
        # img = caffe.io.load_image(os.path.join(image_dir, image))
       
    return inputs


def doClassify(model_def, model_weights, test_dir, test_txt):
    caffe.set_mode_gpu()
    model_def = model_def
    model_weights = model_weights
    predictor = Classifier(model_def, model_weights, image_dims=(512, 512), mean=np.array([103.939, 116.779, 123.68], dtype='float64'))
    inputs = make_inputs(test_dir, test_txt)
    pred = predictor.predict(inputs, oversample=True)
    # print(pred)
    np.save('./rst/prob_1.npy', pred)
    caffe.mpi_fin()


model_def = myself+''
model_weights = ''
test_dir = ''
test_txt = ''
doClassify(model_def, model_weights, test_dir, test_txt)

