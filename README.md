# AI Coding Agent Project

## Overview

This is a demo project for the AI Coding Agent. It serves as a proof of concept to showcase the capabilities of the coding assistant and how to implement an AI agent loop.

## Tools available for the Agent
- List Directories
- Read content of a file
- Write to a file
- Run a python file

## Installation and usage
To install the AI Coding Agent, clone the repository and go inside of the repo and install the required dependencies:

- Example `.env` file:
    ```env
    GEMINI_API_KEY="your-gemoni-api-key"
    ```
    More default configurations are available in the `config/config.py` file

- Once done initialize the vertual env using `uv` and run the application
    ```bash
    uv sync
    source .venv/bin/activate
    uv run main.py "any question to ask to coding agent" --verbose
    ```

## Additional Information

For security purpose the AI coding agent is restricted to only the `calculator` directory via configuration. So any quries and tool calls perfomred by the AI will be limited to that directory only. You can change this with .evn configuration.