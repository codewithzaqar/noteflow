from setuptools import setup, find_packages

setup(
    name="NoteFlow",
    version="0.01",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'noteflow=noteflow.cli:main',
        ],
    },
    author="codewithzaqar",
    description="Simple CLI Journal Tool",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)