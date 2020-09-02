from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()


with open('LICENSE') as f:
    license = f.read()


requirements = ["numpy","wget","scipy","matplotlib","requests"]

setup(
    name="gnssrefl0",
    version="0.0.1",
    author="Kristine M. Larson",
    author_email="kristinem.larson@gmail.com",
    description="GNSS Reflections package",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/kristinemlarson/gnssrefl0/",
    packages=['gnssrefl0'],
    entry_points ={
        'console_scripts': [
            'gnssrefl0 = gnssrefl0.gnssir:main',
            'rinex2snr = gnssrefl0.rinex2snr:main',
            'ymd = gnssrefl0.ymd:main',
            'quickLook = gnssrefl0.quickLook:main',
            'make_json_input = gnssrefl0.make_json_input:main',
            ],
        },
    license=license,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
)
