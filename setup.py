from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='msfs-2020-real-time-weather',
    version='0.1',
    install_requires=['metar'],
    url='https://github.com/svp318/MSFS2020-Real-Time-Weather',
    license='',
    author='Simon Vega',
    author_email='simonvega1990@hotmail.com',
    description='Update a custom Microsoft Flight Simulator weather preset'
                ' with the current conditions of a given airport.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.6'
)
