
# vtk-calculate-projected-area

VTK-based python script for calculating the projected area of a STL file.

It is inspired on the frontal area calculator code by Paul McIntosh
[CalculateFrontalArea.cxx](https://github.com/internetscooter/Vespa-Labs/blob/master/VespaCFD/CalculateFrontalArea/CalculateFrontalArea.cxx)


## How to use

Import the `projectArea` module and call the function `project`.
Stand-alone call to come.


## Dependencies

You only need python and the VTK module.
If numpy is available a faster version of the algorithm is used.

A conda environment can be used. To install it:

```bash
conda create --name calculate-projected-area python=3.8 conda-forge::vtk==9.0.3 conda-forge::libstdcxx-ng
conda activate calculate-projected-area
```

All the packages for running the validation notebook in this repo can be installed
with the environment file `environment.yml` (includes numpy, matplotlib and jupyter):

```bash
conda env create -f environment.yml
conda activate calculate-projected-area
```


## Validation

You may check the validation of the algorithm in the jupyter notebook
`validation.ipynb`. With sufficient resolution the error is lower than 1% 


## TODO

- Make it standalone (easy, just set the argv)
- Set an hybrid argument for defining the vector (`x`,`y`,`z` or the projection vector)
- Add script to produce images to illustrate the algorithm
- Add images to the jupyter notebook
