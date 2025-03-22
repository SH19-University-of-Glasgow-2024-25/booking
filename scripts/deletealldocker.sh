#!/bin/bash

# Reset Docker Environment Script
# WARNING: This will delete ALL Docker containers, images, volumes, and networks!

echo "Starting Docker environment reset..."
echo "This will delete all containers, images, volumes, and networks. Proceed? (y/n)"
read -r confirmation

if [[ "$confirmation" != "y" ]]; then
  echo "Operation canceled."
  exit 0
fi

echo "Stopping all running containers..."
docker stop $(docker ps -q) 2>/dev/null

echo "Removing all containers..."
docker rm $(docker ps -a -q) 2>/dev/null

echo "Removing all images..."
docker rmi $(docker images -q) -f 2>/dev/null

echo "Removing all volumes..."
docker volume rm $(docker volume ls -q) 2>/dev/null

echo "Removing all networks..."
docker network rm $(docker network ls | grep "bridge\|host\|none" -v | awk '{if(NR>1) print $1}') 2>/dev/null

echo "Pruning any dangling resources..."
docker system prune -af --volumes

echo "Docker environment reset complete!"
echo "Next steps: Use 'docker-compose build' or other commands to rebuild from scratch."
