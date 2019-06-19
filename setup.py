from setuptools import setup, find_packages

setup(
    name="hunpy",
    description="Python wrapper for extracting ads.",
    long_description=open("README.rst").read(),
    author="Sisco Puig",
    author_email="sisco@siscopuig.com",

    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hunpy = hunpy.hunpy:main'
        ],
    }

    # url="https://github.com/vprusso/scirate",
    # packages=["hunpy"],
    # version="0.1.0",
    # install_requires=['nose', 'bs4', 'lxml', 'requests'],
    # license="MIT",
    # keywords=["scirate", "scirate API", "scirate python"],
    # classifiers=[
    #     "Development Status :: 4 - Beta",
    #     "Intended Audience :: Developers",
    #     "License :: OSI Approved :: MIT License",
    #     "Natural Language :: English",
    #     "Programming Language :: Python :: 3.5",
    # ],

    # project_urls={
    #     "Homepage": "http://vprusso.github.io/",
    # }
)