FROM python:slim-bullseye
LABEL version=V1.0.0
LABEL app=SAADE-authen-app 
ENV LOG=1
WORKDIR /my_app
COPY . .
RUN  pip install --upgrade pip && pip3 install requests  
CMD ["python3", "authentication.py"]


