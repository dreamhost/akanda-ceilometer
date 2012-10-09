from setuptools import setup, find_packages


setup(
    name='Akanda Ceilometer Plugin',
    version='0.1.0',
    description='Ceilometer plugin for processing Akanda notifications',
    author='DreamHost',
    author_email='dev-community@dreamhost.com',
    url='http://github.com/dreamhost/akanda',
    license='BSD',
    install_requires=[
    ],
    namespace_packages=['akanda'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
