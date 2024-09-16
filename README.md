# drug-release-analysis

Drug release analysis based on different statistical metrics.
This app is deployed to Streamlit cloud - https://drug-release.streamlit.app/.

## Community guidelines

Feel free to clone this repo and use it for your own analysis.
If you like to contribute, please raise a PR. If you have a feature request, please raise an issue with more details.

### Pre-requisites

- Docker

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
# To revert all local changes
git restore .
# To get code changes from remote
git pull --rebase

# To push code changes to remote
git add .
git commit -m "commit message"
git push origin main

```

## Advanced usage - running python from local

This is not required. Optional if you want to run the app locally using python & not docker.

- Python version - `v3.12+`
- [pyenv](https://github.com/pyenv/pyenv) - Simple Python version management
  - Only needed if you have multiple versions of python and want to have a better developer experience.
- [Poetry](https://python-poetry.org) - For python dependency management

## First time setup

```sh
pyenv update # if --list doesn't have updated python versions
pyenv install --list # list available versions that can be installed
pyenv install 3.12.3 # only needed for installing this python
pyenv local 3.12.3  # Activate Python
```

### Development flow

```sh
eval "$(pyenv init --path)"
# install dependencies
poetry install
poetry shell
python -m streamlit run drug_release_analysis/streamlit_app.py

```

## Todo

Capability

- Handling multiple groups
  - Add dropdown to select group
  - Show the selected group data in observation & observation scatter plots
- Cumulative Release
  - Scatter Plot
    - Need to check correctness for multiple groups with valid data
    - Time in hours on x-axis
    - percentage cumulative release on y-axis
    - Add trendline
    - Show equation
    - Show R^2
- Fractional values - is it wrong in the calculated data ? Validate this.
- Higuchi plot
  - Don't focus on this, till the correctness of till now calculations are validated

## References

- trendline calculation - https://plotly.com/python/linear-fits/
