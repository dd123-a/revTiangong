from setuptools import setup, find_packages

# 定义项目的依赖
install_requires = [
    'requests>=2.25.0',        # 假设项目需要requests库
    'websockets>=8.1',         # 假设项目需要websockets库
    'fake_useragent>=0.1.11',   # 假设项目需要fake_useragent库
    'filetype>=1.0.7',         # 假设项目需要filetype库
    'asyncio>=3.4.3',          # 项目使用asyncio，确保版本兼容
]

setup(
    name='revTianGong',
    version='0.1.0',
    author='DrTang',
    description='A Python wrapper for the TianGong chatbot API',
    long_description_content_type='text/markdown',
    url='https://github.com/dd123-a/revTiangong',
    packages=find_packages(),
    install_requires=install_requires,
    python_requires='>=3.6',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            # 如果有可执行的命令行脚本，可以在这里定义
            # 'tiangong-chatbot=tiangong.cli:main',
        ],
    },
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='chatbot tiangong api wrapper',
    zip_safe=False,
)