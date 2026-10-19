import os
from glob import glob
from setuptools import setup

package_name = 'g29_control'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    package_dir={'': 'src'},
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Leyde Calderón Sánchez',
    maintainer_email='leydecs17@gmail.com',
    description='Logitech G29 steering wheel manual control for a CARLA ego vehicle.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'g29_to_carla = g29_control.g29_to_carla_node:main',
            'route_logger = g29_control.route_logger_node:main',
        ],
    },
)
