"""
h5dict - HDF5-based persistent dict
===================================
"""

import numpy as np
import cPickle
import tempfile, os
import collections

import h5py

class h5dict(collections.MutableMapping):
    def __init__(self, path=None, mode='a'):
        '''A persistent dictionary with data stored in an HDF5 file.

        Parameters:
        path : str
            The path to an HDF5 file. If None, than create a temporary file
            that will be deleted with the object.

        mode : str
            'r'  - Readonly, file must exist
            'r+' - Read/write, file must exist
            'w'  - Create file, truncate if exists
            'w-' - Create file, fail if exists
            'a'  - Read/write if exists, create otherwise (default)
        '''
        if path is None:
            tmpfile = tempfile.NamedTemporaryFile(delete=False)
            tmppath = tmpfile.name
            tmpfile.close()
            self.path = tmppath
            self.is_tmp = True
        else:
            self.path = path
            self.is_tmp = False
        self._h5file = h5py.File(self.path, mode)
        self._types = {}
        self._dtypes = {}

    def __contains__(self, key):
        return self._h5file.__contains__(key)

    def __iter__(self):
        return self._h5file.__iter__()

    def __len__(self):
        return len(self.keys())

    def keys(self):
        return self._h5file.keys()

    def __getitem__(self, key):
        if key not in self.keys():
            raise KeyError('\'%s\' is not in the keys' % key)

        value = self._h5file[key].value
        # If it is a single string, then it is a pickled object.
        if isinstance(value, str):
            value = cPickle.loads(value)

        return value

    def __delitem__(self, key):
        self._types.__delitem__(key)
        self._dtypes.__delitem__(key)
        self._h5file.__delitem__(key)
        self._h5file.flush()

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise Exception('h5dict only accepts string keys')
        if key in self.keys():
            self.__delitem__(key)

        if isinstance(value, np.ndarray):
            self._h5file[key] = value
            self._types[key] = type(value)
            self._dtypes[key] = value.dtype
        else:
            self._h5file[key] = cPickle.dumps(value, protocol = -1)
            self._types[key] = type(value)
            self._dtypes[key] = None
        self._h5file.flush()

    def value_type(self, key):
        return self._types[key]

    def value_dtype(self, key):
        return self._dtypes[key]

    def __del__(self):
        self._h5file.close()
        if sel.is_tmp:
            os.remove(self.path)
            
