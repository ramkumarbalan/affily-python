FROM python:3.8

COPY . .

RUN pip install --upgrade pip
# Install Python dependencies
RUN pip install selenium 
RUN pip install requests
RUN pip install flask 
RUN pip install gunicorn 
RUN pip install telegram 
RUN pip install --upgrade pip

# Install necessary packages
RUN apt-get update && apt-get install -y \
    firefox-esr \
    xvfb

# Set up the geckodriver (Firefox driver)
# Download the appropriate version from https://github.com/mozilla/geckodriver/releases
# Make sure to replace the version number in the URL below
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz && \
    tar -xvzf geckodriver-v0.34.0-linux64.tar.gz && \
    mv geckodriver /usr/local/bin && \
    rm geckodriver-v0.34.0-linux64.tar.gz


# Set up a virtual display using xvfb
ENV DISPLAY=:99

EXPOSE 4000

# Command to run Gunicorn with your Flask app
# CMD ["gunicorn", "--bind", "0.0.0.0:4000", "scrap:app", "--workers", "4", "--threads", "4"]

ENV FLASK_APP=scrap.py

CMD ["flask", "run", "--host", "0.0.0.0"]