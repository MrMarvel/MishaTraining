from setuptools import setup, find_packages

setup(
    name='misha-training',
    version='1.0.0',
    packages=['misha_training'],
    url='',
    license='',
    author='Sergey',
    author_email='seregakkk999@yandex.ru',
    description='',
    install_requires=["numpy", "playsound==1.2.2", "pyobjc", "py2app"],
    python_requires=">=3.10",
    include_package_data=True,
    data_files=[('resources', ['resources/ding.mp3', 'resources/mario_death.mp3', 'resources/notification.mp3',
                               'resources/roblox_negative.mp3'])]
)
