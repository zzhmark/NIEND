from setuptools import setup, Extension
import numpy

setup(
    license='MIT',
    ext_modules=[
        Extension(
            'human.img_pca_filter',
            sources=['human/img_pca_filter.pyx'],
            language='c++',
            include_dirs=[numpy.get_include()],
            library_dirs=[],
            libraries=[],
            extra_compile_args=[],
            extra_link_args=[]
            )
    ]
)
