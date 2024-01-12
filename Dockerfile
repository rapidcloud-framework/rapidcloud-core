# Base image
FROM amazon/aws-cli:2.13.30


RUN yum install -y yum-utils

RUN yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo

RUN yum -y install terraform

# Set the working directory
#WORKDIR /app
#
## Install dependencies
#COPY requirements.txt /app
#COPY build.py /app
#RUN ls -la
#RUN pip install -r requirements.txt

#RUN python3 build.py --action build --os macos --skip_disabled_templates --build_stage all 

# Copy application files to the container
#COPY . /app

# Expose port 8000
#EXPOSE 8000

# Set the default command
#CMD ["python", "main.py"]
