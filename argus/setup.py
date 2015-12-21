from setuptools import setup

setup(
    name='argus',
    version='0.1.0',
    description='watch file system events through web sockets.',
    url='git@github.com:TDaglis/argus.git',
    author='Thanasis Daglis, SourceLair PC',
    author_email='ath.daglis@gmail.com',
    license='MIT',
    packages=['argus'],
    scripts=['bin/argus'],
    install_requires=[
        'tornado==4.3',
        'watchdog==0.8.3',
    ]
)
