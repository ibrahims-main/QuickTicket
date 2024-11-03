from setuptools import setup, find_packages

setup(
    name="quickticket",
    version="1.0.0",
    author="Ibrahim Mohsin",
    author_email="codingstudentbruh@gmail.com",
    description='An Easy To Use Discord Ticketing System Library.',
    packages=find_packages(),
    install_requires=[
        'discord.py',
        'chat-exporter',
        'PyGithub',
        'aiosqlite',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)