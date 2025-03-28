from setuptools import setup, find_packages

setup(
    name='pyta4j',
    version='0.1.0',
    description='A Python technical analysis library inspired by TA4J',
    author='quickfox15',
    author_email='quickfox15(at)gmail.com',
    packages=find_packages(include=['pyta4j', 'pyta4j.*']),
    include_package_data=True,
    python_requires='>=3.9',
    install_requires=[
        'pandas',
        'numpy',
        'pytest'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ]
)
