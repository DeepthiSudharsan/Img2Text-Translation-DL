[NOTE : BECAUSE OF INSTALLING THE TRANSFORMERS, THE MEMORY CONSUMED BY THE CODE IS EXCEEDING THE STREAMLIT MEMORY LIMIT, SO THE DEPLOYED APP WILL CRASH ONCE INPUT IS TAKEN. SO IF YOU WANT TO RUN AND SEE THE MAGIC HAPPEN, RUNNING IT LOCALLY ON YOUR SYSTEM IS PREFERED RATHER THAN THE DEPLOYED APP. INSTRUCTIONS TO RUN LOCALLY IS GIVEN HERE]

This app has been deployed on streamlit. To view the app check the link below

https://share.streamlit.io/deepthisudharsan/img2text-translation-dl/main/Img-Text-Translation-Streamlit/img2text_translate.py

## Streamlit web app implementation of the project. 

### Pre-requisites to run Streamlit app locally :

Make sure to install streamlit if haven't already, to install streamlit use the following command :

```
pip install streamlit
```
All the package requirements along with the versions have been mentioned in the requirements.txt file. Running the code is as simple as going to your Anaconda Prompt, navigating to the directly with your streamlit py files, and running the command 
```
$ streamlit run img2text_translate.py
```
### How to run?

* Clone the repository
* Setup Virtual environment
```
$ python3 -m venv env
```
* Activate the virtual environment
```
$ source env/bin/activate
```
* Install dependencies using
```
$ pip install -r requirements.txt
```
* Run Streamlit
```
$ streamlit run img2text_translate.py
```
