# alemira-test

## 1. Environment

Exporting an environment file across platforms
```sh
conda env export --from-history > environment.yml
```

Creating an environment
```sh
conda env create -f environment.yml
```

Updating an environment
```sh
conda env update --file environment.yml  --prune
```