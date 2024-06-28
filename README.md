# drug-release-analysis

Drug release analysis based on different statistical metrics

### Pre-requisites

- Docker
<!-- - Python version - `v3.12+`
- [pyenv](https://github.com/pyenv/pyenv) - Simple Python version management
  - Only needed if you have multiple versions of python and want to have a better developer experience.
- [Poetry](https://python-poetry.org) - For python dependency management -->

<!-- ## First time setup

```sh
pyenv update # if --list doesn't have updated python versions
pyenv install --list # list available versions that can be installed
pyenv install 3.12.3 # only needed for installing this python
pyenv local 3.12.3  # Activate Python
eval "$(pyenv init --path)"
``` -->

## Getting started - running with docker

```sh
# build and run the docker container
docker compose up --build

# Build docker image
# docker build \
#   -t drug-release-analysis:local .
# docker run -p 8501:8501 drug-release-analysis:local

```

## Git commands

```sh
# To get code changes from remote
git pull --rebase

# To push code changes to remote
git add .
git commit -m "commit message"
git push origin main

```

## Advanced usage - running python from local

```sh
poetry install
python -m streamlit run drug_release_analysis/streamlit_app.py
```

## Todo

- https://plotly.com/python/linear-fits/
  - This has trendline calculation
- Standard Curve
  - Scatter Plot
    - Add trendline
    - Show equation
    - Show R^2
- Cumulative Release
  - Scatter Plot
    - Time in hours on x-axis
    - percentage cumulative release on y-axis
    - Add trendline
    - Show equation
    - Show R^2
