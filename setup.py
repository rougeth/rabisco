from setuptools import find_packages, setup


with open('README.md') as f:
    long_description = f.read()


setup(
    name='rabisco',
    url='https://github.com/rougeth/rabisco',
    version='0.2.0',
    description='note cli app',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Marco Rougeth',
    author_email='marco@rougeth.com',
    py_modules=['rabisco', 'cli'],
    entry_points={
        'console_scripts': [
            'r=cli:cli',
            'rabisco=cli:cli',
        ],
    },
    install_requires=[
        'click',
        'python-slugify',
    ],
)
