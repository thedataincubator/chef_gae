#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name="chef_gae",
    version="1.0.3",
    description="A GAE-Friendly wrapper for the chef API",
    url="https://github.com/thedataincubator/chef_gae",
    author="Christian Moscardi",
    author_email="christian@thedataincubator.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7"],
    keywords='google appengine pycrypto chef server devops',
    packages=find_packages(),
    install_requires=['pycrypto==2.6.1', 'requests==2.1.0'])
