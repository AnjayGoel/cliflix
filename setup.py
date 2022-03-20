from setuptools import setup

setup(
    name='cliflix',
    version='1.0',
    packages=['cliflix','cliflix.search'],
    install_requires=[
        'requests',
        'tabulate',
        'lxml'
    ],
    url='',
    license='',
    author='silverbug',
    author_email='anjay.goel@gmail.com',
    description='Search and stream torrents from terminal'
)
