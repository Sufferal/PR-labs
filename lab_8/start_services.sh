#!/bin/bash
PYTHON_INTERPRETER="/home/destiny/Desktop/sem_v/pr/PR-labs/lab_8/raft_venv/bin/python"

for service_number in 1 2 3; do
  SCRIPT_PATH="/home/destiny/Desktop/sem_v/pr/PR-labs/lab_8/service_${service_number}/main.py"
  gnome-terminal --title="Service ${service_number}" --command="${PYTHON_INTERPRETER} ${SCRIPT_PATH}"
done

# Open postman
gnome-terminal --title="Postman" --command="postman"
