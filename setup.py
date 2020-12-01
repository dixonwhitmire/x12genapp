from setuptools import find_packages, setup

setup(
    name='x12genapp',
    author='Dixon Whitmire',
    email='dixon.whitmire@ibm.com',
    description='Integration API Which Maps X12 Transactions to IBM GenApp Services',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask==1.1.2',
        'requests==2.25.0',
        'simplejson==3.17.2'
    ],
    extras_require={
      'test': ['pytest==6.1.2', 'coverage==5.3']
    },
    classifiers=[
        "Domain :: Health Care :: X12"
        "Programming Language :: Python :: 3",
        "License :: Apache 2.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
