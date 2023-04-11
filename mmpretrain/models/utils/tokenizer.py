# Copyright (c) OpenMMLab. All rights reserved.
from typing import Optional

from transformers import AutoTokenizer, BartTokenizer, BertTokenizer

from mmpretrain.registry import TOKENIZER


def register_hf_tokenizer(cls: Optional[type] = None):
    """Register HuggingFace-style tokenizer class."""
    if cls is None:

        # use it as a decorator: @register_hf_tokenizer()
        def _register(cls):
            register_hf_tokenizer(cls=cls)
            return cls

        return _register

    def from_pretrained(**kwargs):
        if ('pretrained_model_name_or_path' not in kwargs
                and 'name_or_path' not in kwargs):
            raise TypeError(
                f'{cls.__name__}.from_pretrained() missing required '
                "argument 'pretrained_model_name_or_path' or 'name_or_path'.")
        # `pretrained_model_name_or_path` is too long for config,
        # add an alias name `name_or_path` here.
        name_or_path = kwargs.pop('pretrained_model_name_or_path',
                                  kwargs.pop('name_or_path'))
        return cls.from_pretrained(name_or_path, **kwargs)

    TOKENIZER._register_module(
        module=from_pretrained, module_name=cls.__name__)
    return cls

register_hf_tokenizer(AutoTokenizer)


@register_hf_tokenizer()
class BLIPTokenizer(BertTokenizer):

    @classmethod
    def from_pretrained(
        cls,
        pretrained_model_name_or_path,
        *init_inputs,
        **kwargs,
    ):
        tokenizer = super().from_pretrained(
            pretrained_model_name_or_path,
            *init_inputs,
            **kwargs,
        )
        tokenizer.add_special_tokens({'bos_token': '[DEC]'})
        tokenizer.add_special_tokens({'additional_special_tokens': ['[ENC]']})
        return tokenizer


@register_hf_tokenizer()
class OFATokenizer(BartTokenizer):

    vocab_files_names = {
        'vocab_file': 'vocab.json',
        'merges_file': 'merges.txt'
    }

    pretrained_vocab_files_map = {
        'vocab_file': {
            'OFA-Sys/OFA-tiny':
            'https://huggingface.co/OFA-Sys/OFA-tiny/blob/main/vocab.json',
            'OFA-Sys/OFA-medium':
            'https://huggingface.co/OFA-Sys/OFA-medium/blob/main/vocab.json',
            'OFA-Sys/OFA-base':
            'https://huggingface.co/OFA-Sys/OFA-base/blob/main/vocab.json',
            'OFA-Sys/OFA-large':
            'https://huggingface.co/OFA-Sys/OFA-large/blob/main/vocab.json',
        },
        'merges_file': {
            'OFA-Sys/OFA-tiny':
            'https://huggingface.co/OFA-Sys/OFA-tiny/blob/main/merges.txt',
            'OFA-Sys/OFA-medium':
            'https://huggingface.co/OFA-Sys/OFA-medium/blob/main/merges.txt',
            'OFA-Sys/OFA-base':
            'https://huggingface.co/OFA-Sys/OFA-base/blob/main/merges.txt',
            'OFA-Sys/OFA-large':
            'https://huggingface.co/OFA-Sys/OFA-large/blob/main/merges.txt',
        },
    }

    max_model_input_sizes = {
        'OFA-Sys/OFA-tiny': 1024,
        'OFA-Sys/OFA-medium': 1024,
        'OFA-Sys/OFA-base': 1024,
        'OFA-Sys/OFA-large': 1024,
    }

    @classmethod
    def from_pretrained(
        cls,
        pretrained_model_name_or_path,
        *init_inputs,
        **kwargs,
    ):
        tokenizer = super().from_pretrained(
            pretrained_model_name_or_path,
            *init_inputs,
            **kwargs,
        )
        tokenizer.add_tokens(['<code_{}>'.format(i) for i in range(8192)])
        tokenizer.add_tokens(['<bin_{}>'.format(i) for i in range(1000)])
        return tokenizer