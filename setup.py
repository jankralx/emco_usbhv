from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name="emco_usbhv",
    version="0.1.0",
    description="A package for controlling EMCO USB HV power supply.",
    long_description=readme,
    author="Jan Kral",
    author_email="jankralx@gmail.com",
    url="https://github.com/jankralx/emco_usbhv",
    packages=find_packages(exclude=["emco_usbhv_app.py"]),
    install_requires=[
        'hidapi',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)