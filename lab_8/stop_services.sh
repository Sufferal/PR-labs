#!/bin/bash

for service_number in 1 2 3; do
  SERVICE_PID=$(pgrep -f "/home/destiny/Desktop/sem_v/pr/PR-labs/lab_8/service_${service_number}/main.py")

  # Check if the service is running
  if [ -n "${SERVICE_PID}" ]; then
    # Terminate the service
    kill -15 "${SERVICE_PID}"
    echo "Service ${service_number} terminated."
  else
    echo "Service ${service_number} is not running."
  fi
done

# Close the terminal
pkill -f "gnome-terminal"
echo "All terminals closed."
