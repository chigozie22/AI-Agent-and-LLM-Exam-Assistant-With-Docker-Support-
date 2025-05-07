FROM nvidia/cuda:12.6.1-base-ubuntu24.04

#set working directory
WORKDIR /app


#install system dependencies 
RUN apt-get update && apt-get install -y \
	build-essential \ 
	libopenblas-dev \
	libgl1 \
	curl \
	tesseract-ocr \
	libsm6 \
	libxext6 \
	libxrender-dev \
	python3 \
	python3-pip \
	python3-venv \
	&& rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

RUN pip3 install --upgrade pip --break-system-packages

#install python dependencies
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

#install cuda specific pytorch
RUN pip3 install --no-cache-dir --break-system-packages torch==2.7.0+cu126 torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu126

	
#copy project files 
COPY . .

#expose ports
EXPOSE 8000
EXPOSE 8501

#start fastapi and Streamlit concurrently
CMD ["bash", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0"]

