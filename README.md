# Air quality data collection system

Enter the development environment with Nix:

```sh
nix-shell
```

The shell provides Python 3.13, pandas, NumPy, SciPy, scikit-learn,
joblib, Matplotlib, Seaborn, JupyterLab, and the sensor dependencies.
It supports CPU model training; start a notebook with:

```sh
jupyter lab
```

To collect readings on a machine with the connected sensors and serial/I2C
device permissions:

```sh
python collect.py
```
