# coding: utf-8
import os
import compileall

filePath = os.path.split(os.path.realpath(__file__))[0]

compileall.compile_dir(filePath)
