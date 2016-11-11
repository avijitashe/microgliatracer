It holds the main executable files written in Python, and it's packages available via Anaconda 2 installation. This is a project for learning purpose only. Please follow the pipeline below to understand the fow of logic.

Pipeline:
1) Read an 3D stack as ndarray
2) Remove salt-n-pepper noise from the whole stack, as one
3) Use median filtering to smooth the stack from abrupt variations
4) Improve the contrast
5) Perform erosion of smaller objects or processes, to prepare the soma for extraction
6) Perform soma segmentation and collect their ocation in 3D space
7) Label the conected regions for a count

to be updated soon.

Thanks you!
