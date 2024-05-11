# MENTORIA - Demo

<div align="center">
  <p align="center">
    <img src="./data/logo 2.png" alt="MENTORIA Logo" />
  </p>
<p align="center">
<strong>Multi-functional Educational Navigator Toolkit for Outstanding Results and Interactive Assistance</strong></p>
</div>



Mentoria is a RAG (Retrieval Augmented Generation) application that enables you to chat with your data from different sources, documents like: `.txt`, `.pdf`, `.doc` and `.docx`, or chat with data from `URL` which can point to **article/blog** or to **Youtube video**. It uses **Gemini** API to serve the user in the background.


Hopefully soon I'll add more options like OpenAI and Cohere and make the choice to the user to use what he prefer. Also adding more options for data sources like `.log` files.

## Table of Contents

- [MENTORIA - Demo](#mentoria---demo)
  - [Table of Contents](#table-of-contents)
  - [Usage](#usage)
  - [Demo](#demo)
  - [Contributions](#contributions)
  - [Contact](#contact)

## Usage


To try **mentoria** locally, follow those steps:

1. Clone the repo:
    ``` bash
    git clone https://github.com/mohamedhassan218/mentoria-demo
    ```


2. Create a virtual environment:
    ```bash
    python -m venv .venv
    ```


3. Activate your virtual environment:
    - On Windows:
        ```bash
        .venv\Scripts\activate
        ```

    - On Unix or MacOS:
        ```bash
        source .venv/bin/activate
        ```


4. Install the dependencies:
    ``` bash
    pip install -r requirements.txt
    ```


5. Set up environment variables:
    Create a `.env` file in the project root and add the following:
    ```
    GOOGLE_API_KEY=""
    ```
    Get your free API key from [here](https://ai.google.dev/gemini-api/docs/api-key)


6. Run the Project:
    ``` bash
    streamlit run main.py
    ```


## Demo

<div align="center">
<p align="center">Chat with website</p>
  <p align="center">  
    <img src="./data/Example 1.png" alt="Chat with website example" />
  </p>
</div>


<div align="center">
<p align="center">Chat with document</p>
  <p align="center">  
    <img src="./data/Example 2.png" alt="Chat with document example" />
  </p>
</div>


## Contributions

Contributions are highly appreciated! If you have any additional features, ideas or suggestions for improvements, please don't hesitate to submit a pull request. Also, feel free to take the code, customize it and try different ideas.

## Contact

- <a href="mailto:m.hassan.def@gmail.com">Gmail</a>
- <a href="https://www.linkedin.com/in/mohamed218hassan/">Linkedin</a>