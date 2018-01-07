#!/usr/bin/env bash
# Change to the project root directory. Assume this file is at scripts/.
cd $(dirname ${BASH_SOURCE[0]})/../

# Some constants
CAFFE_DIR=/mnt/lustre/yangkunlin/sensenet_disp/example
train_model() {
  local solver=/mnt/lustre/yangkunlin/kaggle_camera/inceptionResNetV2/incepResV2/incepResV2_AddFC_solver.prototxt
  local log=/mnt/lustre/yangkunlin/kaggle_camera/inceptionResNetV2/incepResV2/model_AddFC/log/incepResV2_AddFC.log
  # export LD_LIBRARY_PATH=/mnt/lustre/share/cuda-7.5/lib64:$LD_LIBRARY_PATH
  export LD_LIBRARY_PATH=/mnt/lustre/share/libboost/lib:$LD_LIBRARY_PATH
  mkdir -p $(dirname ${log})

  MV2_USE_CUDA=1 MV2_ENABLE_AFFINITY=0 MV2_SMP_USE_CMA=0 \
  GLOG_vmodule=MemcachedClient=-1 srun -p Zgf \
  --mpi=pmi2 --gres=gpu:8 -n8 --ntasks-per-node=8 --job-name=ipr2_fc \
  ${CAFFE_DIR}/build/tools/caffe train --solver=${solver} --weights=/mnt/lustre/yangkunlin/kaggle_camera/inceptionResNetV2/inceptionResNetV2.caffemodel  2>&1|tee ${log}
}
train_model