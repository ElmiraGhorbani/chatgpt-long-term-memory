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
    description='Empower your projects with a large knowledge base and adaptive memory using Chatgpt Long Term Memory.',
    long_description='The Chatgpt Long Term Memory package is designed to empower your projects by accommodating a large number of simultaneous users while leveraging an extensive knowledge base and adaptive memory. This capability is made possible through the integration of cutting-edge technologies, including GPT (OpenAI), llama vector index, and Redis datastore.',    packages=find_packages(),
    install_requires=[
        'redis-chatgpt>=0.1.2',
        'llama-index>=0.7.9',
        'openai>=0.27.8'
    ],
    project_urls=project_urls,
    long_description=long_description,
    long_description_content_type='text/markdown'
)