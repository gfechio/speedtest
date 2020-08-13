FROM arm32v7/alpine
RUN apk add --no-cache gcc bash wget git \
	  py-pip python3 python3-dev \
    && rm -rf /var/cache/apk/*

RUN pip install --upgrade pip setuptools wheel
RUN mkdir /src
ADD src/ /src/
RUN pip install --upgrade pip \
	&& pip install -r src/requirements.txt
ENV APP_DIR /src
CMD ["python3", "/src/main.py"]
