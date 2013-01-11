from setuptools import setup, find_packages

setup(
    name='akanda-ceilometer',
    version='0.1.0',
    description='Ceilometer plugin for processing Akanda notifications',
    author='DreamHost',
    author_email='dev-community@dreamhost.com',
    url='http://github.com/dreamhost/akanda',
    license='BSD',
    install_requires=['ceilometer'],
    namespace_packages=['akanda'],
    packages=find_packages(),
    entry_points={
        'ceilometer.collector': [
            'akanda_bandwidth = akanda.ceilometer.notifications'
            ':NetworkBandwidthNotification',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    )
