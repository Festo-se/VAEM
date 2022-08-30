from setuptools import setup, find_packages

setup(
    name='VaemModule',  # Required

    version='0.0.2',  # Required

    description='Software for controlling the VAEM Festo valve control module',  # Optional

    #long_description=long_description,  # Optional

    long_description_content_type='text/markdown',  # Optional (see note above)

    author='Festo',  # Optional

    author_email='milen.kolev@festo.com',  # Optional

    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Liquid Handling :: hardware control',

        'License :: Apache',

        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    keywords='VAEM, liquid handler, setuptools, festo',  # Optional

    #package_dir={'': 'Src'},  # Optional

    packages=find_packages(),  # Required

    python_requires='>=3.8, <4',

    install_requires=[  'pymodbus>=2.5.0',
                        'pydantic>=1.8.2',
                        'typing>=3.7.4.3',
                        'python-multipart==0.0.5',
                        'jsonschema'
    ],  # Optionals

    # data_files=[('config_schema', ['config/move_schema.json'])],  # Optional

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    #entry_points={  # Optional
    #    'console_scripts': [
    #        'sample=sample:main',
    #    ],
    #},

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/Festo-se/VAEM/issues',
        'Source': 'https://github.com/Festo-se/VAEM',
    },
)