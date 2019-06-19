<p align="center">
<img src="doc/_images/veros-logo-400px.png?raw=true">
</p>

<p align="center">
  <a href="http://veros.readthedocs.io/?badge=latest">
    <img src="https://readthedocs.org/projects/veros/badge/?version=latest" alt="Documentation status">
  </a>
  <a href="https://travis-ci.org/dionhaefner/veros">
    <img src="https://travis-ci.org/dionhaefner/veros.svg?branch=master" alt="Build status">
  </a>
  <a href="https://codecov.io/gh/dionhaefner/veros">
    <img src="https://codecov.io/gh/dionhaefner/veros/branch/master/graph/badge.svg" alt="Code Coverage">
  </a>
  <a href="https://zenodo.org/badge/latestdoi/87419383">
    <img src="https://zenodo.org/badge/87419383.svg" alt="DOI">
  </a>
</p>

ECOSYS3D is a powerful tool that makes high-performance ocean ecosystem modeling approachable and fun. Since
it is a pure Python module, the days of struggling with complicated
model setup workflows, ancient programming environments, and obscure
legacy code are finally over.

ECOSYS3D supports both a NumPy backend for small-scale problems and a fully
parallelized high-performance backend [powered by
Bohrium](https://github.com/bh107/bohrium) using either OpenMP (CPU) or
OpenCL (GPU), and runs on distributed architectures via MPI.

A good starting point to gain an overview of ECOSSYS3D\' design,
performance, and capabilities are [these slides of a talk on
ECOSSYS3D](http://slides.com/dionhaefner/veros-ams) held during the 98th
Annual Meeting of the American Meteorological Society.

The underlying numerics are based on
[pyOM2](https://wiki.cen.uni-hamburg.de/ifm/TO/pyOM2), an ocean model
developed by Carsten Eden (Institut für Meereskunde, Hamburg
University). ECOSSYS3D is currently being developed at Niels Bohr Institute,
Copenhagen University.

#### How about a demonstration?

<p align="center">
  <a href="https://media.giphy.com/media/dwS6EeA4OTfsZZHVE9/giphy.mp4">
      <img src="https://media.giphy.com/media/dwS6EeA4OTfsZZHVE9/giphy-downsized-large.gif" alt="0.25×0.25° high-resolution model spin-up">
  </a>
</p>

<p align="center">
(0.25×0.25° high-resolution model spin-up, click for better
quality)
</p>

## Features

ECOSSYS3D provides

-   a fully staggered **3-D grid geometry** (*C-grid*)
-   support for both **idealized and realistic configurations** in
    Cartesian or pseudo-spherical coordinates
-   several **friction and advection schemes** to choose from
-   isoneutral mixing, eddy-kinetic energy, turbulent kinetic energy,
    and internal wave energy **parameterizations**
-   several **pre-implemented diagnostics** such as energy fluxes,
    variable time averages, and a vertical overturning stream function
    (written to netCDF output)
-   **pre-configured idealized and realistic set-ups** that are ready to
    run and easy to adapt
-   **accessibility, readability, and extensibility** - thanks to the
    power of Python!

## ECOSSYS3D for the impatient

A minimal example to install and run ECOSSYS3D:

```bash
$ pip install veros[all]
$ veros copy-setup acc --to /tmp
$ cd /tmp/acc
$ python acc.py
```

## Installation

### Dependencies

ECOSSYS3D only has one external library dependency, `HDF5`. The installation
procedure of this library varies between platforms. The easiest way to
install ECOSSYS3D and its dependencies (including Bohrium) is [Anaconda
Python](https://www.continuum.io/downloads) that ships with a package
manager (`conda`).

If you do not want to use Anaconda, the most convenient way is to use
your operating system\'s package manager. On Debian / Ubuntu, you can
e.g. use

```bash
$ sudo apt-get install libhdf5-dev
```

Similar package managers on OSX are [Homebrew](https://brew.sh/) or
[MacPorts](https://www.macports.org/), which both provide the required
dependencies as pre-compiled binaries.

### Installing ECOSSYS3D

As soon as you have a working environment, installing ECOSSYS3D is simple:

1.  Clone the repository to your hard-drive:

    ```bash
    $ git clone https://github.com/cbrockw/ecosys3D.git
    ```

2.  Install it, preferably with

    ```bash
    $ pip install -e ecosys3D
    ```

    If you use the `-e` flag, any changes you make to the model code are
    immediately reflected without having to re-install.

In case you want to use the Bohrium backend, you will have to install
[Bohrium](https://github.com/bh107/bohrium), e.g. through `conda` or
`apt-get`, or by building it from source.
