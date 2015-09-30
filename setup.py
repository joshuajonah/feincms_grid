from setuptools import setup, find_packages
from feincms_grid import __version__ as version
import os

README = os.path.join(os.path.dirname(__file__), 'README')

with open(README) as fobj:
    long_description = fobj.read()

setup(name="feincms-grid",
    version=version,
    description="Integrate Foundation columns with FeinCMS contenttypes",
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='django feincms foundation framework columns grid',
    author='Joshua Jonah',
    author_email='joshuajonahcom@gmail.com',
    url='http://github.com/joshuajonah/feincms_grid',
    license='BSD',
    packages=find_packages(),
    install_requires=['Django>=1.7', 'FeinCMS>=1.10.1'],
    include_package_data=True,
    zip_safe=False
)