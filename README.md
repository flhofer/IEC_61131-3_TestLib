# CoDeSys-TestLib
A CoDeSys v2.3 test library based on a POU approach

The aim of this work was to create a standardized, IEC 61131-3 and cross-vendor usable software testing library. With it, developers should have a new production tool which allows fast in-environment testing.

## Directory structure
- _AutoGen_           Python scripts to automate test case generation for direct import into CoDeSys from an Excel file (WIP)
- _Library_           Testing library, exports and `.lib` file
  - FUNCFIRSTVER.EXP  contains a simple POU 1-1 test version
  - utf.lib           testing libary
- _Examples_          Example projects using the testing library for CoDeSys v2.3

## Documentation

This work is based on my [Master's Thesis](https://florianhofer.it/docmisc/?id=6e2867cb785616c1680bc344faf0b76f2a5b6134) and a [IEEE Trasnactions on Industrial Informatics](https://florianhofer.it/papers/?id=191d675eb3b37b0ee9bfe6022777b137a6127972) journal paper published in September 2019. 
It is still work in progress, but unfortunately only a side project of my ongoing PhD, so please support the project by contributing or sponsorship.

Thank you!
