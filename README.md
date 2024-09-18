# Postman-CTF
This challenge is designed to help you explore how the web works, with a primary focus on the HTTP Protocol using Postman to interact with web APIs and understand various concepts related to HTTP, or Web cybersecurity. You can access a live version of this challenge on https://postman-ctf-d527648a9cbe.herokuapp.com/.

## Overview
This challenge is aimed for people with no knowledge to biggener level knowledge of Web technologies and/or cybersecurity. It consists of 10 levels of hidden flags that you can find through completing a series of steps. Your goal is to find all the flags and submit them through the '/submitflags' path. The challenges cover various aspects of web technologies, including HTML, HTTP, Cookies, Encoding and more!

## Pre-requisites
1. [Postman API application](https://www.postman.com/downloads/) or [Postman API web version](https://go.postman.co)
2. [Python](https://www.python.org/downloads/) (Only for running application locally, if using the live version on hekoru then there is no need for python)

## Usage
To run it locally follow these steps steps:
1. Clone the repository
```bash
git clone https://github.com/heshamalmosawi/Postman-CTF
```
2. Create virtual environment
```bash
python3 -m venv <env_name>
```
3. Activate virtual environment
```bash
source <env_name>/bin/activate
```
4. Install the required dependencies
```bash
pip install -r requirements.txt
```
5. Run the python application
```bash
python3 main.py
```

## Contributors
- [Sayed Hesham Al-Mosawi](https://github.com/heshamalmosawi)
- [Hashem Alzaki](https://github.com/SnakeSees)