# Misc commands

Installing `requirements.txt` using `conda`.

```
conda install --yes --file requirements.txt
```

Installing `requirements.txt` using `pip`.

```
pip install -r requirements.txt
```

Find location of the python package `site`

```
python -c "import site; print(site.getsitepackages())"
```