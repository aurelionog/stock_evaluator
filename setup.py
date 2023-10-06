from setuptools import setup, find_packages

setup(
    name='stock_evaluator',
    version='1.0.0',
    description='A Python tool for stock analysis',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/aurelionog/stock_evaluator',
    packages=find_packages(),
    install_requires=[
        'yfinance',
        'pandas',
        'numpy',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
    ],
    entry_points={
        'console_scripts': [
            'stock-analysis = main_code.main:main',  # Replace with your module and main function
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
