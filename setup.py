from setuptools import setup, find_packages
import os


def read_requirements(file_name):
    file_name = os.path.abspath(file_name)  # Convert to absolute path
    requirements = []
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('-r') or line.startswith('--requirement'):
                # Recursively read referenced requirements file
                referenced_file = line.split(maxsplit=1)[1]
                requirements.extend(read_requirements(os.path.join(os.path.dirname(file_name), referenced_file)))
            elif line and not line.startswith('#'):  # Ignore comment lines
                requirements.append(line)
    return requirements


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='xpuls-mlmonitor',
    version='0.0.8',
    author='Sai Sharan Tangeda',
    author_email='saisarantangeda@gmail.com',
    description='Automated telemetry and monitoring for ML & LLM Frameworks',
    license='Apache License 2.0',
    url='https://github.com/xpuls-labs/xpuls-mlmonitor-python',
    packages=find_packages(),
    install_requires=read_requirements('requirements.txt'),
    extras_require={
        'langchain': read_requirements('requirements/requirements_langchain.txt'),
        'all': read_requirements('requirements.txt')
    },
    long_description_content_type='text/markdown',
    long_description=long_description,
)
