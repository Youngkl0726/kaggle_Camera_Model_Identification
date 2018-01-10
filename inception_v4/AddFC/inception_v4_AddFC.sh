#!/usr/bin/env bash
# Change to the project root directory. Assume this file is at scripts/.
cd $(dirname ${BASH_SOURCE[0]})/../

# export LD_LIBRARY_PATH=/mnt/lustre/share/nccl-7.5/lib:$LD_LIBRARY_PATH
# Some constants
CAFFE_DIR=/mnt/lustre/yangkunlin/caffe_kaggle

exp=/mnt/lustre/yangkunlin/kaggle_camera/inception_v4
 # local pretrained_model=$2
solver=${exp}/inception_v4_AddFC_solver.prototxt
log=${exp}/log/inception_v4_AddFC.log

  mkdir -p $(dirname ${log})

  MV2_USE_CUDA=1 MV2_ENABLE_AFFINITY=0 MV2_SMP_USE_CMA=0 srun -p Zgf \
  --gres=gpu:8 -n1 --ntasks-per-node=1 --job-name=icp4fc \
  ${CAFFE_DIR}/build/tools/caffe train --solver=${solver} \
  --weights=/mnt/lustre/yangkunlin/kaggle_camera/inception_v4/inception_v4.caffemodel \
  --gpu=0,1,2,3,4,5,6,7  2>&1|tee ${log}

