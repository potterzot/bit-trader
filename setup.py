from distutils.core import setup

setup(
    name='BitTrader',
    version='0.1.0',
    author='Nicholas Potter',
    author_email='potter.nichoas@gmail.com',
    packages=['bittrader', 'bittrader.lib', 'bittrader.test'],
    #scripts=['bin/bittrader.py'],
    url='http://pypi.python.org/pypi/BitTrader/',
    license='LICENSE.txt',
    description='Standardized Bitcoin APIs with trading interface.',
    long_description=open('README.md').read(),
    #install_requires=[ json
    #     
    #    
    #    #"Django >= 1.1.1",
    #    #"caldav == 0.1.4",
    #],
    
)
