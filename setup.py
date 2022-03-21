#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='bimbangal',
    version='0.1.0',
    description=('Bimbangal Backend'),
    long_description='',
    url='https://github.com/chocoogirl/bimbangal_backend',
    author='Suganya',
    author_email='suganyachandrasekar27@gmail.com',
    license='Apache v2',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers, Managers, Interviewers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='',
    packages=find_packages(),
    install_requires=[
        'falcon==1.4.1',
        'gunicorn==19.6.0',
        'aumbry[yaml]==0.7.0',
        'docopt==0.6.2',
        'certifi==2018.4.16',
        'chardet==3.0.4',
        'idna==2.7',
        'mongoengine==0.15.3',
        'protobuf==3.6.0',
        'pymongo==3.7.1',
        'python-dotenv==0.8.2',
        'python-mimeparse==1.6.0',
        'redis==2.10.6',
        'requests==2.19.1',
        'six==1.11.0',
        'urllib3==1.23',
        'waitress==2.1.1',
        'walrus==0.5.1'
    ],
    package_data={},
    data_files=[],
    entry_points={
        'console_scripts': [
            'bimbangal = src.__main__:main'
        ],
    },
)
