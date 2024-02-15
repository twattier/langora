from setuptools import setup, find_packages
setup(
    name='langora',
    version='1.0',
    author='Thierry Wattier',
    description='Web scraping for knowledge base system',    
    url='https://github.com/twattier/langora',
    keywords='GenAI, Scraping, RAG, LLM',
    packages=find_packages(include=['app.*']),
)