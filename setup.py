"""
	setup
	~~~~~~

	:license: BSD, see LICENSE for details.
	:author: David Casado Martinez <dcasadomartinez@gmail.com>
"""


import os
from setuptools import setup, find_packages
from mpiece import __version__


filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.rst')
with open(filepath, 'r') as f:
	long_description = f.read()

# TODO: Cambiar url

setup(
	name="mpiece",
	version=__version__,
	packages=find_packages(include=('mpiece',)),
	author="David Casado Martínez",
	author_email="dcasadomartinez@gmail.com",
	description="Customizable and fast Markdown parser in pure Python",
	long_description=long_description,
	url='https://github.com/davidnotplay/mpiece',
	platforms="any",
	license="BSD",
	zip_safe=False,
	keywords="markdown html parser",
	test_suite="tests",
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: Implementation :: PyPy',
		'Topic :: Text Processing :: Markup',
		'Topic :: Software Development :: Libraries :: Python Modules',
	]
)
