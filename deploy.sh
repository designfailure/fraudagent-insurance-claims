#!/bin/bash
# FraudAGENT - Automated Deployment Script
# Deploys the application using Docker Compose

set -e  # Exit on error

echo "================================================================================"
echo "  FraudAGENT - Automated Deployment Script"
echo "================================================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed!${NC}"
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi
echo -e "${GREEN}✓ Docker is installed${NC}"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed!${NC}"
    echo "Please install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose is installed${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    echo "Creating .env from template..."
    cp .env.template .env
    echo -e "${RED}❌ Please edit .env file with your API keys before continuing!${NC}"
    echo ""
    echo "Required variables:"
    echo "  - KUMO_API_KEY"
    echo "  - OPENAI_API_KEY"
    echo ""
    read -p "Press Enter after you've updated .env to continue..."
fi

# Validate API keys are set
source .env
if [[ "$KUMO_API_KEY" == "your-kumo-api-key-here" ]] || [[ "$OPENAI_API_KEY" == "your-openai-api-key-here" ]]; then
    echo -e "${RED}❌ API keys not configured in .env file!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ API keys configured${NC}"

# Check if data directory exists
if [ ! -d "data" ]; then
    echo -e "${YELLOW}⚠️  data/ directory not found${NC}"
    echo "Creating data directory..."
    mkdir -p data
    echo -e "${YELLOW}Please add your Parquet data files to the data/ directory${NC}"
fi

# Stop existing containers
echo ""
echo "Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Build and start containers
echo ""
echo "Building Docker image..."
docker-compose build

echo ""
echo "Starting containers..."
docker-compose up -d

# Wait for application to start
echo ""
echo "Waiting for application to start..."
sleep 5

# Check if container is running
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}✅ Application deployed successfully!${NC}"
    echo ""
    echo "================================================================================"
    echo "  APPLICATION READY"
    echo "================================================================================"
    echo ""
    echo "Access the application at:"
    echo "  • Local: http://localhost:7860"
    echo "  • Network: http://$(hostname -I | awk '{print $1}'):7860"
    echo ""
    echo "To view logs:"
    echo "  docker-compose logs -f"
    echo ""
    echo "To stop the application:"
    echo "  docker-compose down"
    echo ""
else
    echo -e "${RED}❌ Application failed to start${NC}"
    echo "Check logs with: docker-compose logs"
    exit 1
fi
