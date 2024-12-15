import os
import json
import torch
from functools import wraps
from typing import Optional
from collections import defaultdict
import argparse

class MLSnapshot:

    def __init__(self, base_dir: str):
        # Parse the command-line argument if provided
        parser = argparse.ArgumentParser(description='MLSnapshot command-line argument parser.')
        parser.add_argument('--mlsnapshot', type=str, help='Additional folder name to append to the base directory')
        args, _ = parser.parse_known_args()  # Use parse_known_args to allow other args
        
        # Determine the snapshot directory
        if args.mlsnapshot:
            self.snapshot_dir = os.path.join(args.mlsnapshot,base_dir)
            os.makedirs(self.snapshot_dir, exist_ok=True)
        else:
            self.snapshot_dir = None
        
        self.inc = defaultdict(int)

    def __call__(self, func):
        if not self.snapshot_dir:
            # If snapshot_dir is not set, return the original function
            return func
        @wraps(func)
        def wrapper(*args, **kwargs):

            dirname=os.path.join(self.snapshot_dir,func.__name__,str(self.inc[func.__name__]))
            os.makedirs(dirname,exist_ok=True)

            # Serialize inputs
            input_data = {'args': self._serialize(args,dirname), 'kwargs': self._serialize(kwargs,dirname)}
            input_path = os.path.join(dirname, f"input.json")
            with open(input_path, 'w') as f:
                json.dump(input_data, f)

            output=func(*args, **kwargs)

            # Execute function
            output_data = self._serialize(output,dirname)

            # Serialize output
            output_path = os.path.join(dirname, f"output.json")
            with open(output_path, 'w') as f:
                json.dump(output_data, f)

            self.inc[func.__name__]+=1

            return output

        return wrapper

    def _serialize(self, obj, dirname):
        if isinstance(obj, (list, tuple)):
            return [self._serialize(o,dirname) for o in obj]
        elif isinstance(obj, dict):
            return {k: self._serialize(v,dirname) for k, v in obj.items()}
        elif isinstance(obj, torch.Tensor):
            tensor_path = os.path.join(dirname, f"tensor_{id(obj)}.pt")
            torch.save(obj, tensor_path)
            return {'type': 'tensor', 'path': tensor_path}
        elif isinstance(obj, (int, float, str, bool, type(None))):
            return obj
        elif isinstance(obj, Optional):
            return self._serialize(obj.value,dirname)
        else:
            raise TypeError(f"Unsupported type: {type(obj)}")

    @classmethod
    def retrieve(cls, snapshot_dir, func_name: str):
        funcpath=os.path.join(snapshot_dir,func_name)
        n=len(os.listdir(funcpath))
        rv=[None for _ in range(n)]
        for i in os.listdir(funcpath):
            filepath=os.path.join(funcpath,i)
            input_path = os.path.join(filepath, f"input.json")

            # Load input data
            with open(input_path, 'r') as f:
                input_data = json.load(f)

            args = cls._deserialize(input_data['args'])
            kwargs = cls._deserialize(input_data['kwargs'])

            output_path = os.path.join(filepath, f"output.json")

            # Load output data
            with open(output_path) as fp:
                jf=json.load(fp)
                output = cls._deserialize(jf)

            rv[int(i)]=(args, kwargs, output)
        return rv

    @classmethod
    def _deserialize(cls, obj):
        if isinstance(obj, list):
            return [cls._deserialize(o) for o in obj]
        elif isinstance(obj, dict):
            if obj.get('type') == 'tensor':
                return torch.load(obj['path'])
            return {k: cls._deserialize(v) for k, v in obj.items()}
        else:
            return obj