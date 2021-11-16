
import os
from os.path import dirname

from setuptools import find_packages, setup


def get_file_contents(filename):
    with open(os.path.join(dirname(__file__), filename)) as fp:
        return fp.read()


def get_install_requires(requirement_file):
    requirements = get_file_contents(requirement_file)
    install_requires = []

    for line in requirements.split('\n'):
        line = line.strip()

        if line and not line.startswith('-'):
            install_requires.append(line)
    return install_requires

setup(
    name="quartic-sdk",
    description="QuarticSDK is the SDK package which exposes the APIs to the user",
    long_description=get_file_contents('README.md'),
    long_description_content_type='text/markdown',
    license='MIT',
    author="Quartic.ai engineering team",
    author_email="tech@quartic.ai",
    url="https://github.com/Quarticai/QuarticSDK/",
    keywords=["Quartic", "QuarticSDK"],
    classifiers=[
        'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3.9', #Specify which python versions that you want to support
    ],
    install_requires=get_install_requires('requirements.txt'),
    extras_require={
        "complete": get_install_requires('requirements.txt') + get_install_requires('model_requirements.txt')
    },
    include_package_data=True,
    packages=find_packages(exclude=['tests*'])
    )
