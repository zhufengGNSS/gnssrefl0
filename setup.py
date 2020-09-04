from setuptools import setup, find_packages

with open("README.rst", "r") as readme_file:
    readme = readme_file.read()

requirements = ["numpy","wget","scipy","matplotlib","requests"]

setup(
    name="gnssrefl0",
    version="0.0.6",
    long_description=readme,
    long_description_content_type="text/x-rst",
    author="Kristine M. Larson",
    author_email="kristinem.larson@gmail.com",
    description="GNSS Reflections package",
    url="https://github.com/kristinemlarson/gnssrefl0/",
    packages=find_packages(),
    include_package_data=True,
    entry_points ={
        'console_scripts': [
            'gnssir_test= gnssrefl0.gnssir_cl:main',
            'rinex2snr = gnssrefl0.rinex2snr:main',
            'ymd = gnssrefl0.ymd:main',
            'quickLook = gnssrefl0.quickLook:main',
            'download_rinex = gnssrefl0.download_rinex:main',
            'make_json_input = gnssrefl0.make_json_input:main',
            ],
        },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    install_requires=requirements,
)
