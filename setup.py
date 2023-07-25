from setuptools import find_packages, setup
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

project_urls = {
  'Github': 'https://github.com/ElmiraGhorbani/chatgpt-long-term-memory',
}

setup(
    name='chatgpt_long_term_memory',
    version='0.1.0',
    author='Elmira Ghorbani',
    description='The ChatGPT Long Term Memory package is a powerful tool designed to empower your projects with the ability to handle a large number of simultaneous users. ',
    packages=find_packages(),
    install_requires=[
        'redis-chatgpt>=0.1.2',
        'llama-index>=0.7.9',
        'openai>=0.27.8',
        'tiktoken>=0.4.0'
    ],
    project_urls=project_urls,
    long_description=long_description,
    long_description_content_type='text/markdown'
)