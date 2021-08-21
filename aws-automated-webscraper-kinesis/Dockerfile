#FROM python:3.7

#COPY . /tmp/scraper/
#WORKDIR /tmp/scraper
#RUN pip install -r requirements.txt

#CMD ["python3", "main.py"]

FROM python:3.8.6-buster

COPY . /tmp/scraper/
WORKDIR /tmp/scraper

# ensure local python is preferred over distribution python
# ENV PATH /usr/local/bin:$PATH


# cleanup tarballs and downloaded package files
RUN pip install --upgrade pip \
	&& pip install numpy pandas beautifulsoup4 boto3 requests tweepy\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/
	
CMD ["python3", "main.py"]
