from setuptools import setup, find_packages

setup(
    name="hunpy",
    description="Python wrapper for extracting ads.",
    long_description=open("README.rst").read(),
    author="Sisco Puig",
    author_email="sisco@siscopuig.com",
    url="https://github.com/siscopuig/hunpy",
    version="0.0.1",
    # install_requires=['nose', 'bs4', 'lxml', 'requests'],
    license="MIT",
    keywords=["hunpy", "hunpy python"],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hunpy = hunpy.hunpy:main'
        ]
    }

)