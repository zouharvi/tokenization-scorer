import setuptools

setuptools.setup(
    name='tokenization-scorer',
    version='1.0.1',
    author='Vilém Zouhar',
    author_email='vzouhar@ethz.ch',
    description=('Package for evaluating text tokenizations.'),
    long_description="""
        Simple package for evaluating text tokenizations. The input is a text (list of files or stdin) and output a single number.
        The higher the number, the better the tokenization.
        The intended workflow is to try multiple tokenizations and select the one with the highest number.
    """,
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
