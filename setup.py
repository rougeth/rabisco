from setuptools import find_packages, setup


setup(
    name='rabisco',
    url='https://github.com/rougeth/rabisco',
    author='Marco Rougeth',
    author_email='marco@rougeth.com',
    py_modules=['rabisco', 'cli'],
    entry_points={
        'console_scripts': ['r=cli:cli'],
    },
    install_requires=[
        'click',
        'python-slugify',
    ],
)
