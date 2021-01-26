from setuptools import setup, find_packages

with open("AutoClip/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='AutoClip',
    version='0.1.0',
    packages=['AutoClip'],
    url='https://github.com/shiv213/AutoClip',
    license='MIT',
    author='Shiv Trivedi',
    author_email='shiv.v.trivedi@gmail.com',
    description='AutoClip',
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False
)
