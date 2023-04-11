# Copyright (c) OpenMMLab. All rights reserved.
from pathlib import Path
from typing import List

import mmengine
from mmengine.fileio import get_file_backend

from mmpretrain.registry import DATASETS
from .base_dataset import BaseDataset


@DATASETS.register_module()
class COCOCaption(BaseDataset):
    """COCO Caption dataset.

    Args:
        ann_file (str): Annotation file path.
        data_root (str): The root directory for ``data_prefix`` and
            ``ann_file``. Defaults to ''.
        data_prefix (str | dict): Prefix for training data. Defaults to ''.
        pipeline (Sequence): Processing pipeline. Defaults to an empty tuple.
        **kwargs: Other keyword arguments in :class:`BaseDataset`.
    """

    def load_data_list(self) -> List[dict]:
        """Load data list."""
        img_prefix = self.data_prefix['img_path']
        annotations = mmengine.load(self.ann_file)
        file_backend = get_file_backend(img_prefix)

        data_list = []
        for ann in annotations:
            data_info = {
                'image_id': Path(ann['image']).stem.split('_')[-1],
                'img_path': file_backend.join_path(img_prefix, ann['image']),
                'gt_caption': ann['caption'],
            }

            data_list.append(data_info)

        return data_list