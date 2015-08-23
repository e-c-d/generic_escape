from setuptools import setup
pkg = "generic_escape"
ver = '1.1.0'
setup(name             = pkg,
      version          = ver,
      description      = "A simple library for escaping and unescaping strings",
      author           = "Eduard Christian Dumitrescu",
      license          = "LGPLv3",
      url              = "https://github.com/e-c-d/generic_escape",
      packages         = [pkg],
      install_requires = [],
      classifiers      = ["Programming Language :: Python :: 3 :: Only"])
