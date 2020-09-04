from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()


with open('LICENSE') as f:
    license = f.read()


requirements = ["numpy","wget","scipy","matplotlib","requests"]

setup(
    name="gnssrefl0",
    version="0.0.5",
    author="Kristine M. Larson",
    author_email="kristinem.larson@gmail.com",
    description="GNSS Reflections package",
    long_description=readme,
    long_description_content_type='text/markdown',
    url="https://github.com/kristinemlarson/gnssrefl0/",
    packages=find_packages(),
    package_data={'gnssrefl0': ['gpt_1wA.pickle']},
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
    license=license,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
)
