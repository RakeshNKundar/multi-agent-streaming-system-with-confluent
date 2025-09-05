#!/usr/bin/env bash
set -euo pipefail

echo "Starting installation of required tools..."

# Detect OS
OS="$(uname -s || echo Windows)"
case "$OS" in
    Linux*)     PLATFORM=linux;;
    Darwin*)    PLATFORM=mac;;
    MINGW*|MSYS*|CYGWIN*|Windows*) PLATFORM=windows;;
    *)          echo "Unsupported OS: $OS" && exit 1;;
esac

#################################
# Install Python3 (>3.9)
#################################
install_python() {
    if [[ "$PLATFORM" == "mac" ]]; then
        brew install python
    elif [[ "$PLATFORM" == "linux" ]]; then
        sudo apt-get update && sudo apt-get install -y python3 python3-pip
    else
        echo "Installing Python (Windows)..."
        winget install -e --id Python.Python.3.11 || choco install -y python
    fi
}

#################################
# Install Terraform CLI
#################################
install_terraform() {
    if [[ "$PLATFORM" == "mac" ]]; then
        brew tap hashicorp/tap
        brew install hashicorp/tap/terraform
    elif [[ "$PLATFORM" == "linux" ]]; then
        sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl
        curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
        echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
        sudo apt-get update && sudo apt-get install -y terraform
    else
        echo "Installing Terraform (Windows)..."
        winget install -e --id HashiCorp.Terraform || choco install -y terraform
    fi
}

#################################
# Install Confluent Cloud CLI
#################################
install_confluent() {
    if [[ "$PLATFORM" == "mac" ]]; then
        brew install confluentinc/tap/cli
    elif [[ "$PLATFORM" == "linux" ]]; then
        curl -sL --fail https://cnfl.io/cli | sh -s -- -b /usr/local/bin
    else
        echo "Installing Confluent CLI (Windows)..."
        winget install -e --id Confluentinc.CLI || choco install -y confluent
    fi
}

#################################
# Install MongoDB Database Tools
#################################
install_mongo_tools() {
    if [[ "$PLATFORM" == "mac" ]]; then
        brew tap mongodb/brew
        brew install mongodb-database-tools
    elif [[ "$PLATFORM" == "linux" ]]; then
        wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
        echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
        sudo apt-get update && sudo apt-get install -y mongodb-database-tools
    else
        echo "Installing MongoDB Database Tools (Windows)..."
        winget install -e --id MongoDB.DatabaseTools || choco install -y mongodb-database-tools
    fi
}

#################################
# Run installers
#################################
install_python
install_terraform
install_confluent
install_mongo_tools

echo "Installation complete! Versions installed:"
python3 --version || python --version
terraform -version | head -n1 || echo "Terraform not found"
confluent version || echo "Confluent not found"
mongodump --version || echo "MongoDB tools not found"
