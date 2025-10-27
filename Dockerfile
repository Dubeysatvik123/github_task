FROM ubuntu:22.04
RUN apt update && apt install python3 python3-pip pip -y
WORKDIR /GENAI
COPY . .
RUN pip install -r requirements.txt
CMD ["python3","project1.py"]