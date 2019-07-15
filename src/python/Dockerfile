FROM python:3.6.9-slim 

ADD ./cli_new /mesos/cli
ADD ./lib /mesos/lib
WORKDIR /mesos/cli/

# Install GCC
RUN apt-get update
RUN apt-get install -y gcc

# Install pip requirements 
RUN pip install -r /mesos/cli/pip-requirements.txt
RUN echo "/mesos/cli/lib" > /usr/local/lib/python3.6/site-packages/cli.pth
# Remove gcc to keep the image clean
RUN apt-get purge -y gcc

# Create config for mesos-cli
RUN mkdir /root/.mesos
RUN touch /root/.mesos/config.toml
ENV PATH="/mesos/cli/bin:${PATH}" 
