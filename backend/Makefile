# Makefile

# Define the main target
all: check_python main_task install_requirements create_blob_paths

# Rule to check if Python is installed on Linux or Windows
check_python:
ifeq ($(OS),Windows_NT)
	@python --version >nul 2>&1 && (echo Python is installed) || (echo Python is not installed. Aborting. && exit 1)
else
	@command -v python3 >/dev/null 2>&1 && (echo "Python is installed") || { echo "Python 3 is not installed. Aborting." >&2; exit 1; }
endif

# Define the main task to create the virtual environment
main_task:
ifeq ($(OS),Windows_NT)
	@if exist venv ( \
		echo "Virtual environment already exists. Exiting."; \
		exit 1; \
	) else ( \
		echo "Creating virtual environment"; \
		python -m venv venv; \
	)
else
	@if [ -d "venv" ]; then \
		echo "Virtual environment already exists. Exiting."; \
		exit 1; \
	else \
		echo "Creating virtual environment"; \
		python3 -m venv venv; \
	fi
endif

# Define the task to install requirements
install_requirements: main_task
ifeq ($(OS),Windows_NT)
	@echo "Activating virtual environment and installing requirements"
	@venv\Scripts\pip install -r requirements.txt
else
	@echo "Activating virtual environment and installing requirements"
	@. venv/bin/activate && pip install -r requirements.txt
endif

# Define the task to create blob paths
create_blob_paths:
ifeq ($(OS),Windows_NT)
	@echo "Creating blob paths"
	@if not exist blob\media (mkdir blob\media)
	@if not exist blob\text (mkdir blob\text)
	@if not exist blob\misc (mkdir blob\misc)
	@echo "Creating finished"
else
	@echo "Creating blob paths"
	@mkdir -p blob/media blob/text blob/misc
	@echo "Creating finished"
endif