FROM python:3.8-slim

# Install basic toolchains
RUN apt-get update -qq \
    && apt-get install --no-install-recommends --yes \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install packages that do not require compilation.
RUN python3 -m pip install --no-cache-dir \
    numpy scipy pandas
