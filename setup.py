try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup

    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

setup(
    name="backend-helper",
    version="0.0.1",
    url='https://github.com/mattpaletta/backend-helper-py',
    packages=find_packages(),
    zip_safe=True,
    include_package_data=True,
    install_requires=["psycopg2"],
    setup_requires=[],
    author="Matthew Paletta",
    author_email="mattpaletta@gmail.com",
    description="Helpful package for writing common backend distributed systems",
    license="BSD",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications',
    ]
)
