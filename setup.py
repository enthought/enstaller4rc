from setuptools import setup


with open("README", "rt") as fp:
    DESCRIPTION = fp.read()


setup(
    name="enstaller4rc",
    version="0.0.1dev",
    summary="Small, bundleable library to parse enstaller4rc files.",
    description=DESCRIPTION,
    license="BSD",
    author="David Cournapeau",
    author_email="davidc@enthougth.com",
    packages=["enstaller4rc", "enstaller4rc.tests"],
)
