from setuptools import setup, find_packages

__version__ = '0'

with open('LICENSE.txt') as f:
    license = f.read()

setup(
    name='TradingTools',
    version=__version__,
    author='Rob Innes Hislop',
    author_email='robinneshislop@gmail.com',
    license=license,
    packages=find_packages(),
    url = 'https://github.com/innes213/TradingTools',
    description='Various tools that analyze and screen equities',
    long_description='Various tools that analyze and screen equities',
    install_requires=['numpy',
                      'finsymbols',
                      'pyhoofinance'
                      ]
)
