# chaos-mesh-failure-injector

This tool generates desired yaml files to inject certain failures with [Chaos Mesh](https://chaos-mesh.org/).

## 1. Environment

Create an environment
```sh
conda env create -f environment.yml
```

Activate conda environment
```sh
conda activate cmfi
```

## 2. Quick Start

```sh
python -m app.main
```

## 3. Test

```sh
python -m pytest --cov=app tests
```