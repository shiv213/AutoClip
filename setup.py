from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='AutoClip',
    version='0.1.0',
    packages=find_packages(include='AutoClip'),
    url='https://github.com/shiv213/AutoClip',
    license='MIT',
    include_package_data=True,
    author='Shiv Trivedi',
    author_email='shiv.v.trivedi@gmail.com',
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    zip_safe=False
)
