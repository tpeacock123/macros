This is how to make the scale factor tables for neut:
1) take a very large sample of data generated with NEUT_HADRON_SCATTER_GEN
2) put the name of this file in the input file variable in the cpp file in 2d_histogram_gen/src, change event number if needed
3) recompile
4) run
5) take this input file, put the name of this in the 2d_histo_slices_irregular_bin.py file and run from the build directory
6) This makes the table. Done. 
