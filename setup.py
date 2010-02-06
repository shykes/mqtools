
from setuptools import setup

setup(name='mqtools',
      version='0.0.1',
      author='Solomon Hykes <solomon.hykes@dotcloud.com>',
      install_requires=['argparse', 'carrot'],
      package_dir = {'mqcat' : '.'},
      packages=['mqcat'],
      scripts=['bin/mqcat', 'bin/mqsniff']
)
