from setuptools import setup, Extension

functions_module = Extension(
    name="StrEngine",
    sources=["StrEngine.cpp"],
    extra_compile_args=["-O3", "-fPIC"],
    include_dirs=["/home/grx/.conda/envs/strcpp/lib/python3.10/site-packages/pybind11/include"],
)

setup(ext_modules=[functions_module])
