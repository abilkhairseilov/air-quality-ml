# Air quality ML

Enter the development environment with Nix:

```sh
nix-shell
```

Interactive sessions start Zsh and load your existing `~/.zshrc` (or
`$ZDOTDIR/.zshrc` if you set `ZDOTDIR`), including your aliases, prompt, and
plugins. Commands passed through `nix-shell --run` remain non-interactive.

The shell provides Python 3.13, pandas, NumPy, SciPy, scikit-learn,
joblib, Matplotlib, Seaborn, JupyterLab, and the sensor dependencies.
It supports CPU model training; start a notebook with:

```sh
jupyter lab
```

Load the recorded data in a notebook:

```python
import pandas as pd

data = pd.read_csv("purifier.csv", parse_dates=["timestamp"])
data = data.sort_values("timestamp").reset_index(drop=True)
data.head()
```

Choose a prediction target before training. For forecasting, use earlier
readings for training and later readings for evaluation to avoid leaking future
information. There is no training script yet.

To plot the recordings:

```sh
python visualize_purifier.py
```

To collect readings on a machine with the connected sensors and serial/I2C
device permissions:

```sh
python collect.py
```

Dependencies in this shell come from your configured `nixpkgs`; their versions
are not pinned to `requirements.txt`. No pip install is needed inside the shell.
