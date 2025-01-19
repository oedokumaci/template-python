# Use an official Python runtime as a parent image
FROM python:3.13

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Install PDM (Python Dependency Manager)
RUN pip install pdm

# Install dependencies and pre-commit hooks
RUN make setup

# Run the command to start the app
CMD make run
