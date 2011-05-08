""" unittest package """
import os, re, sys

mainSrc = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'src')
sys.path.append(mainSrc)