import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='tokenization-scorer',
    version='1.0.0',
    author='Vilém Zouhar',
    author_email='vzouhar@ethz.ch',
    description=('Package for evaluating tokenization quality'),
    long_description=long_description,
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
