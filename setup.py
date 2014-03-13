from setuptools import setup

setup(
    name="half-population",
    version="0.1.0",
    author="Rory McCann",
    author_email="rory@technomancy.org",
    py_modules=['half-population'],
    platforms=['any',],
    requires=[],
    license="GPLv3+",
    entry_points={
        'console_scripts': [
            'half-population = half-population:main',
        ]
    },
    classifiers=[
    ],
)
