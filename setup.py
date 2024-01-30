from setuptools import setup

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

exec(open("fs_node_hash/__init__.py").read())

setup(
    name='fs-node-hash',
    version=__version__,
    include_package_data=True,
    python_requires='>=3',
    description='Hash file contents, directories and strings with sha256',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Markus Peitl",
    author_email='office@markuspeitl.com',
    url="https://github.com/markuspeitl/fs-node-hash",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries"

    ],
    install_requires=['hashlib'],
    entry_points={},
    packages=['fs_node_hash']
)
