#!/bin/bash

echo "Setting up DuoCoursa..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is required but not installed. Please install Python3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is required but not installed. Please install pip3 first."
    exit 1
fi

# Install Python dependencies
echo "Installing Python dependencies..."
cd backend
pip3 install -r requirements.txt

# Install Ollama if not already installed
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl https://ollama.ai/install.sh | sh
fi

# Pull the Mistral model
echo "Pulling Mistral model (this may take a while)..."
ollama pull mistral

# Start Ollama service
echo "Starting Ollama service..."
ollama serve &

# Wait for Ollama to start
sleep 5

# Start the backend server
echo "Starting backend server..."
cd backend
python3 -m uvicorn main:app --reload --port 8000 &

# Build and run the Java frontend
echo "Building and running Java frontend..."
cd ../frontend
mvn clean package
java -jar target/duocoursa-cli-1.0-SNAPSHOT-jar-with-dependencies.jar

echo "Setup complete! DuoCoursa is now running."
echo "Backend API is available at: http://localhost:8000"
echo "Use the Java CLI to interact with the application."
