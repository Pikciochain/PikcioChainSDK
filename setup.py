from setuptools import setup, find_packages

version = '2.0.5'

with open('./requirements.txt', 'r') as requirements_file:
    requirements = [
        requirement for requirement in requirements_file
    ]

with open('./dev_requirements.txt', 'r') as dev_file:
    dev_requirements = [
        dev_requirement
        for dev_requirement in dev_file
        if not dev_requirement.startswith('-r') and dev_requirement != '\n'
    ]

setup(
    name='pikciosdk',
    version=version,
    description='Open Source Python SDK of the PikcioChain',
    url='https://gitlab.com/pikciochain/python-sdk',
    author='Pikcio SA',
    author_email='jorick.lartigau@pikcio.com',
    license='Apache2',
    keywords=["SDK", "Blockchain", "Pikcio"],
    packages=find_packages(exclude=['distrib', 'doc', 'tests*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=requirements,
    setup_requires=dev_requirements,
    tests_require=dev_requirements,
)
