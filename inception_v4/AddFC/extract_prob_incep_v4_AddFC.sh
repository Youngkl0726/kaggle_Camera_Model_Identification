#!/usr/bin/env bash
# Change to the project root directory. Assume this file is at scripts/.
cd $(dirname ${BASH_SOURCE[0]})/../

# Some constants

CAFFE_DIR=/mnt/lustre/yangkunlin/caffe_kaggle
export PYTHONPATH=/mnt/lustre/yangkunlin/caffe_kaggle/python:$PYTHONPATH
MODELS_DIR=/mnt/lustre/yangkunlin/kaggle_camera/inception_v4

extract_features() {

  local trained_model=$1

  local result_dir=/mnt/lustre/yangkunlin/kaggle_camera/inception_v4/rst
  rm -rf ${result_dir}
  mkdir -p ${result_dir}
  echo ${result_dir}
  # Extract train, val, test probe, and test gallery features.
  for num in 0 ; do
    echo "Extracting No. ${num} set"
    local num_samples=$(wc -l /mnt/lustre/yangkunlin/kaggle_camera/data/test${num}.txt | awk '{print $1}')
    local num_iters=$(((num_samples + 9) / 10))
    local model=/mnt/lustre/yangkunlin/kaggle_camera/inception_v4/temp_inception_v4_AddFC_test.prototxt
    local list=test${num}
    sed -e "s/\${list}/${list}/g" \
      ${MODELS_DIR}/inception_v4_AddFC_test.prototxt > ${model}
    echo ${model}
    MV2_USE_CUDA=1 MV2_ENABLE_AFFINITY=0 MV2_SMP_USE_CMA=0 \
      srun -p AD2 --gres=gpu:1 -n1 --ntasks-per-node=1 --kill-on-bad-exit=1\
      ${CAFFE_DIR}/build/tools/extract_features \
      ${trained_model} ${model} prob \
      ${result_dir}/prob_${num}_lmdb \
      ${num_iters} lmdb GPU
    srun -p AD2 python2 /mnt/lustre/yangkunlin/kaggle_camera/inception_v4/convert_lmdb_to_numpy.py \
      ${result_dir}/prob_${num}_lmdb ${result_dir}/prob_${num}.npy \
      --truncate ${num_samples}
  done
}


trained_model=/mnt/lustre/yangkunlin/kaggle_camera/inception_v4/model_AddFC/incep_v4_iter_35000.caffemodel

  

extract_features ${trained_model}


# Market1501 cuhk01 cuhk03 3dpes ilids prid viper Dukemtmc-reid SenseReID
# Market1501-test cuhk01 cuhk03 3dpes ilids prid viper SenseReID