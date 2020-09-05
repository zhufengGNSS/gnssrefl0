from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["numpy","wget","scipy","matplotlib","requests"]

setup(
    name="gnssrefl0",
    version="0.0.7",
    author="Kristine Larson",
    author_email="kristinem.larson@gmail.com",
    description="A package to do not much ",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/kristinemlarson/gnssrefl0/",
    packages=find_packages(),
    entry_points ={ 
        'console_scripts': [ 
            'gnssir = gnssrefl0.gnssir_cl:main',
            'rinex2snr = gnssrefl0.rinex2snr_cl:main',
            'quickLook= gnssrefl0.quickLook_cl:main',
            'download_rinex = gnssrefl0.download_rinex:main',
            'make_json_input = gnssrefl0.make_json_input:main',
            ], 
        },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
