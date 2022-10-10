from setuptools import find_packages, setup

setup(
    name="tm1fileutils",
    version="0.1.4",
    description="Tools for working with files created by a TM1 database",
    py_modules=["tm1-file-utils"],
    install_requires=["chardet"],
    extras_require={
        "test": ["pytest"],
    },
    author_email="sutcliffe.alex@gmail.com",
    url="http://github.com/scrambldchannel/tm1-file-utils",
    packages=find_packages(),
    keywords="tm1",
    classifiers=["Development Status :: 3 - Alpha"],
)
