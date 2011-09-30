'''
Created on July 1, 2011

@author: ppa
'''
from setuptools import setup
from setupCommand import TestCommand, CleanCommand

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
        'PyDispatcher>=2.0.1',
        'xlwt>=0.7.2',
        'xlrd>=0.7.1',
        'matplotlib>=0.99',
        'numpy>=1.5.1',
        'BeautifulSoup>=3.2.0',
        'hbase-thrift>=0.20.4'
      ],
      cmdclass = {'test': TestCommand, 'clean': CleanCommand }
)
