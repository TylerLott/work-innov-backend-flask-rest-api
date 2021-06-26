# Specify Base Image
FROM opencvcourses/opencv:440 

# Set working dir
WORKDIR /app

# Install Dependencies
RUN apt-get update
RUN apt-get install tesseract-ocr -y
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . .

# Default Commands
CMD ["flask", "run", "--host", "0.0.0.0"]
