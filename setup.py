from distutils.core import setup

setup(
	name='scratchnet',
	packages=['scratchnet'],
	version='{{VERSION_PLACEHOLDER}}',
	license='MIT',
	description='External server support for scratch projects.',
	author='synicalmx',
	url='https://github.com/synicalmx/scratchnet',
	download_url='https://github.com/synicalmx/scratchnet/archive/scratchnet-0.1.0.tar.gz',
	keywords=['scratch', 'server', 'multiplayer'],
	install_requires=[
		'scratchconnect',
		'profanity',
		'requests',
		'colorama'
	],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
	],
)
