from setuptools import setup, find_packages

setup(
      name='tdatrade',
      version='0.3',
      url='https://github.com/darno63/tdatrade.git',
      packages=find_packages(),
      install_requires=['requests', 'websockets']
)
