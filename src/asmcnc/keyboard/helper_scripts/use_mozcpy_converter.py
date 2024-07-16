# -*- coding: utf-8 -*-
import sys
import mozcpy

converter = mozcpy.Converter()
print(converter.convert(sys.argv[1], n_best=10))