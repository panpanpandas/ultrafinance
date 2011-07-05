from setuptools import setup
import sys, os

version = '1.0.0'

setup(name='ultrafinance',
      version=version,
      description="python project for finance: realtime data collection, analyze, algorithmic trading",
      long_description="""""",
      classifiers=[
        "Development Status :: 1 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
      ],
      keywords='python, Finance, Algorithm, Trading, Realtime, QuantLib, pydispather',
      author='Pan Pan',
      author_email='panpandas@gmail.com',
      url='http://code.google.com/p/ultra-finance/',
      license='MIT',

      packages=['ultrafinance'],
      include_package_data=True,
      install_requires=[
        'xlwt>=0.7.2',
        'xlrd>=0.7.1',
        'numpy>=1.5.1',
        'scipy>=0.9.0rc3'
      ]
)