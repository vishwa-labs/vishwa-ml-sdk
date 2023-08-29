from setuptools import setup, find_packages


def read_requirements(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file if line.strip()]


setup(
    name='xpuls-mlmonitor',
    version='0.0.1',
    author='Sai Sharan Tangeda',
    author_email='saisarantangeda@gmail.com',
    description='Automated telemetry and monitoring for ML & LLM Frameworks',
    license='Apache License 2.0',
    url='https://github.com/xpuls-labs/xpuls-mlmonitor-python',
    packages=find_packages(),
    install_requires=read_requirements('requirements.txt'),
    extras_require={
        'langchain': read_requirements('requirements/langchain_requirements.txt'),
        'all': read_requirements('requirements.txt')
    }
)
