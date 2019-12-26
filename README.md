# CoDeSys-TestLib
A CoDeSys v2.3 test library based on a POU approach

The aim of this work was to create a standardized, IEC 61131-3 and cross-vendor usable software testing library. With it, developers should have a new production tool which allows fast in-environment testing. It is focussed on practitioners needs and does not require further training or programming.

The project phases are as follows:
1. A testing library for CoDeSys and other IEC 61131-3 compatible enviroments
1. An automatic test generation tool to translate input tables into test to be imported
1. Plugins for test vaule detection, input partitioning, border value detection and alike
1. Logging and central processing of test results

## Directory structure
- _AutoGen_           Python scripts to automate test case generation for direct import into CoDeSys from an Excel file (WIP)
- _Library_           Testing library, exports and `.lib` file
  - FUNCFIRSTVER.EXP  contains a simple POU 1-1 test version
  - utf.lib           testing libary
  - *.xml             PlcOpen compatible exports to port the laibrary to other IEC 61131-3 based systems 
- _Examples_          using the testing library for CoDeSys v2.3

## Documentation

This work is based on my [Master's Thesis](https://www.florianhofer.it/docmisc/?id=6e2867cb785616c1680bc344faf0b76f2a5b6134) and a [IEEE Trasactions on Industrial Informatics](https://www.florianhofer.it/papers/?id=191d675eb3b37b0ee9bfe6022777b137a6127972) journal paper published in September 2019. 
It is still work in progress, but unfortunately only a side project of my ongoing PhD, so please support the project by contributing (or sponsorship.. coming soon, fingers crossed!).

Thank you!
