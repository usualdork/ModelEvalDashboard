# ModelEvalDashboard

A powerful and user-friendly PyQt6-based application designed to facilitate the comparison of responses from multiple Large Language Models (LLMs) provided by Hugging Face. This tool enables users to log in, select and manage different models, input custom prompts, and generate and save detailed responses for analysis and comparison.

**Accelerate AI Model Evaluation: Fetch Responses from Multiple Models at Once with a Single Prompt**<br>
**Unlock Time Savings & Informed Decision: Making with Our Intuitive GUI Application**
<br>
<br>

**Table of Contents**


1. [Overview](#overview)
2. [Key Benefits](#key-benefits)
3. [Features](#features)
4. [Dependencies](#dependencies)
5. [Setup and Installation](#setup-and-installation)
6. [Running the Application](#running-the-application)
7. [Usage](#usage)
8. [Important Considerations](#Important-Considerations)
9. [Troubleshooting](#troubleshooting)
10. [Credits](#credits)
11. [License](#license)

## Overview


ModelEvalDashboard is a revolutionary GUI application designed to streamline the evaluation of Large Language Models (LLMs). Our innovative platform enables users to input a **single prompt** and simultaneously fetch responses from **multiple AI models**, saving valuable time and providing a broader range of choices for informed decision-making.

<div align="center">
  <img src="https://github.com/user-attachments/assets/b9c35e5d-977c-4de2-a9d4-3050fead0df1" alt="Interface">
  <p><strong>User Interface</strong></p>
</div>


## Key Benefits


* **Time Efficiency**: Evaluate multiple LLMs with a single prompt, reducing the time spent on individual model queries
* **Increased Choice**: Receive a diverse set of responses from various models, empowering you to make more informed decisions
* **Simplified Comparison**: Easily compare responses side-by-side within our intuitive dashboard

## Features


* **Multi-Model Support**: Fetch responses from multiple LLM models with a single prompt
* **User Authentication**: Log in using your Hugging Face credentials.
* **Single-Prompt Input**: Enter your question or prompt once, and receive responses from all selected models
* **Material Design**: Modern and intuitive user interface with Material Design styling.
* **Side-by-Side Comparison**: Easily evaluate and compare responses within our user-friendly dashboard
* **Customizable Response Length**: Choose from short, medium, or detailed response lengths
* **Response Saving**: Save generated responses to a text file for future reference

## Dependencies


* **Python 3.8+**: [Download from Python.org](https://www.python.org/downloads/)
* **PyQt6**: `pip install pyqt6`
* **Unofficial Hugging Chat API**: `pip install hugchat-api`
    + See [https://github.com/Soulter/hugging-chat-api](https://github.com/Soulter/hugging-chat-api) for API details
* **Required Python Libraries**:
    + `requests`: `pip install requests`
    + `json`: (included with Python)

## Setup and Installation


1. **Clone the Repository**:
    * `git clone https://github.com/usualdork/ModelEvalDashboard.git`
2. **Navigate to the Project Directory**:
    * `cd ModelEvalDashboard`
3. **Create a Virtual Environment (Optional but Recommended)**:
    * `python -m venv venv` (on Windows) or `python3 -m venv venv` (on macOS/Linux)
    * `venv\Scripts\activate` (on Windows) or `source venv/bin/activate` (on macOS/Linux)
4. **Install Dependencies**:
    * `pip install -r requirements.txt`

## Running the Application


1. **Ensure Dependencies are Installed**:
    * Verify all dependencies are installed correctly
2. **Run the Application**:
    * `python main.py` (from the project directory)
3. **Launch the GUI**:
    * The ModelEvalDashboard GUI will launch automatically

  <div align="center">
  <img src="https://github.com/user-attachments/assets/500d4b4f-50c9-4c4e-b59e-21f7d7c9ae77" alt="Interface">
  <p><strong>Dashboard in action</strong></p>
  </div>
  

## Usage


1. **Login**:
    * Enter your email and password to authenticate via the Hugging Chat API
2. **Model Selection**:
    * Choose two or more LLM models for simultaneous response generation
3. **Prompt Input**:
    * Enter your question or prompt in the designated text area (once for all selected models)
4. **Generate Responses**:
    * Click to fetch responses from all selected models with a single prompt
5. **Compare Responses**:
    * Evaluate and compare responses side-by-side in the response panel
6. **Save Responses**:
    * Optionally save responses to a text file for later reference
  
<div align="center">
  <img src="https://github.com/user-attachments/assets/eb9921a9-ca60-4553-8408-286f55970959" alt="Interface">
  <p><strong>Response Saved as .txt</strong></p>
</div>



<div align="center">
  <img src="https://github.com/user-attachments/assets/4a81e232-3ca6-40b8-9c02-a81fa29b2bc1" alt="Interface">
</div>


  
## Important Considerations

### Fair Use and Misuse


- **Fair Use**: This application is intended for educational and personal use. Please ensure that your use of the Hugging Face complies with their terms of service.
- **No Misuse**: Do not use this application for any commercial or unauthorized purposes.

### Performance Limitations

- **Response Time**: Responses might occasionally slow down due to technical limitations and the performance of the Hugging Face API.
  

## Troubleshooting


* **Dependency Issues**:
    + Reinstall dependencies using `pip install -r requirements.txt`
* **API Authentication Errors**:
    + Verify email and password for accuracy
    + Check API service status
* **Application Crashes**:
    + Submit an issue on GitHub with detailed error logs

## Credits


* **Application Development**:  [usualdork](https://github.com/usualdork)
* **Coding Assistance**:  Claude 3.5 Sonnet 
* **Unofficial Hugging Chat API**:  [Soulter (developer of the API used in this application)](https://github.com/Soulter/hugging-chat-api)

## License


This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
