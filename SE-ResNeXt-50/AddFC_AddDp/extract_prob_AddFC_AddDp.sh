#!/usr/bin/env bash
# Change to the project root directory. Assume this file is at scripts/.
cd $(dirname ${BASH_SOURCE[0]})/../

# Some constants
CAFFE_DIR=/mnt/lustre/yangkunlin/sensenet_disp/example
export PYTHONPATH=/mnt/lustre/yangkunlin/sensenet_disp/core/python:$PYTHONPATH
MODELS_DIR=/mnt/lustre/yangkunlin/kaggle_camera/SE-ResNeXt-50/AddFC_AddDp


extract_features() {

  local trained_model=$1

  local result_dir=/mnt/lustre/yangkunlin/kaggle_camera/SE-ResNeXt-50/rst
  rm -rf ${result_dir}
  mkdir -p ${result_dir}
  echo ${result_dir}
  # Extract train, val, test probe, and test gallery features.
  for num in 0 ; do
    echo "Extracting No. ${num} set"
    local num_samples=$(wc -l /mnt/lustre/yangkunlin/kaggle_camera/data/test${num}.txt | awk '{print $1}')
    local num_iters=$(((num_samples + 9) / 10))
    local model=/mnt/lustre/yangkunlin/kaggle_camera/SE-ResNeXt-50/AddFC_AddDp/temp_SE-ResNeXt-50_AddFC_AddDp_test.prototxt
    local list=test${num}
    sed -e "s/\${list}/${list}/g" \
      ${MODELS_DIR}/SE-ResNeXt-50_AddFC_AddDp_test.prototxt > ${model}
    echo ${model}
    MV2_USE_CUDA=1 MV2_ENABLE_AFFINITY=0 MV2_SMP_USE_CMA=0 \
      srun -p Test --gres=gpu:1 -n1 --ntasks-per-node=1 --kill-on-bad-exit=1\
      ${CAFFE_DIR}/build/tools/extract_features \
      ${trained_model} ${model} prob \
      ${result_dir}/prob_${num}_lmdb \
      ${num_iters} lmdb GPU
    srun -p Test python2 /mnt/lustre/yangkunlin/kaggle_camera/SE-ResNeXt-50/convert_lmdb_to_numpy.py \
      ${result_dir}/prob_${num}_lmdb ${result_dir}/prob_${num}.npy \
      --truncate ${num_samples}
  done
}


trained_model=/mnt/lustre/yangkunlin/kaggle_camera/SE-ResNeXt-50/model_AddFC_AddDp/SE-ResNeXt-50_AddFC_iter_60000.caffemodel

  

extract_features ${trained_model}

