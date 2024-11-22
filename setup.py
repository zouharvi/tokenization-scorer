import setuptools

setuptools.setup(
    name='tokenization-scorer',
    version='1.1.6',
    author='Vilém Zouhar',
    author_email='vzouhar@ethz.ch',
    description=('Package for evaluating text tokenizations.'),
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/zouharvi/tokenization-scorer',
    packages=['tokenization_scorer'],
    entry_points={
        'console_scripts': [
            'tokenization-scorer=tokenization_scorer:entry',
            'tokenization_scorer=tokenization_scorer:entry'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3'
    ],
)
