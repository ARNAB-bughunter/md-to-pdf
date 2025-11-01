
# Vulnerability Assessment and Remediation Progress – Docker Images

## Initial Findings
During the vulnerability scan of our Docker images, the following issues were identified:

- **Medium severity**: 490  
- **High severity**: 42  
- **Critical severity**: 2  

---

## Remediation Steps Taken

### 1. Base Image Upgrade
- Upgraded the Docker base image from **UBI 9** to **UBI 10**.  
- This reduced the number of vulnerabilities significantly.  

### 2. Python Upgrade Attempt
- Evaluated upgrading from **Python 3.11** to **Python 3.12**.  
- This was not feasible because several of our core libraries (e.g., **TensorFlow, NumPy**) do not yet support Python 3.12 or have compatibility issues.  
- **Decision:** Dropped the Python 3.12 upgrade and reverted to Python 3.11.  

### 3. Library-Level Issues
- While sticking to **Python 3.11**, identified that the **Keras library** introduces a **High severity vulnerability**.  
- **Current status:** Further action required (evaluate patch, alternative version, or mitigation).  

---

## Current Status
- Base image vulnerabilities largely mitigated by moving to **UBI 10**.  
- Python version locked at **3.11** for compatibility reasons.  
- One **High severity vulnerability** remains due to the **Keras library**.  

---

## Package Inventory
Below is the full list of Python dependencies.  
Packages with **known issues / unupgradable** are marked in **<span style="color:red">red</span>**



- absl-py==2.1.0
- aiofiles==24.1.0
- annotated-types==0.7.0
- astunparse==1.6.3
- calamari_ocr==2.3.1
- certifi==2024.12.14
- dataclasses-json==0.6.7
- editdistance==0.8.1
- flatbuffers==25.1.24
- fuzzywuzzy==0.18.0
- gast==0.4.0
- google-auth==2.38.0
- google-auth-oauthlib==1.0.0
- google-pasta==0.2.0
- grpcio==1.74.0
- grpcio-tools==1.74.0
- h5py==3.12.1
- httpx==0.28.1
- idna==3.10 
- <span style="color:red">keras==2.12.0</span>
- langdetect==1.0.9
- lazy_loader==0.4
- Levenshtein==0.26.1
- lxml==5.3.0
- marshmallow==3.26.0
- memory-profiler==0.61.0
- mypy-extensions==1.0.0
- nltk==3.9.1 
- <span style="color:red">numpy==1.23.5</span>
- opencv-contrib-python==4.11.0.86
- opencv-python==4.11.0.86
- opt_einsum==3.4.0
- packaging==24.2
- paiargparse==1.1.2 
- <span style="color:red">pandas==2.2.3</span>
- pdf2image==1.17.0
- pillow==11.1.0
- prettytable==3.13.0
- protobuf==6.32.0
- psutil==7.0.0
- pydantic==2.11.7
- pydantic_core==2.33.2
- pymqi==1.12.11
- python-bidi==0.6.3
- python-dateutil==2.9.0.post0
- pytz==2024.2
- PyYAML==6.0.2
- pyzbar==0.1.9
- RapidFuzz==3.11.0
- regex==2024.11.6
- requests==2.32.3
- scikit-image==0.25.1
- scipy==1.15.1
- six==1.17.0 
- <span style="color:red">tensorflow==2.12.0</span>
- <span style="color:red">tensorflow-serving-api==2.12.0</span>
- termcolor==2.4.0 
- <span style="color:red">tfaip==1.2.6</span>
- timeout-decorator==0.5.0
- tqdm==4.67.1
- typeguard==4.4.1
- typing-inspect==0.9.0
- typing-inspection==0.4.1
- typing_extensions==4.14.1
- urllib3==2.3.0
- wrapt==1.14.1


