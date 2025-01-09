#!/bin/bash

# Set up permissions
sudo chown -R vscode:vscode /home/vscode/.vscode-server

# Install Python requirements
pip3 install --user -r requirements.base.txt

# Install development requirements
pip3 install --user pytest pytest-cov black flake8 isort

# Verify cypher-shell installation
if ! command -v cypher-shell &> /dev/null; then
    echo "Installing cypher-shell..."
    wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
    echo "deb https://debian.neo4j.com stable latest" | sudo tee /etc/apt/sources.list.d/neo4j.list
    sudo apt-get update
    sudo apt-get install -y cypher-shell
fi

# Set up git configuration
git config --global pull.rebase false
git config --global core.autocrlf input