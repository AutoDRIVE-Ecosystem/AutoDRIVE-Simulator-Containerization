####################################################
#
#   AutoDRIVE API/Devkit Dockerfile
#
####################################################

FROM python:3.8.10

WORKDIR /app

# Install display drivers
RUN apt update && apt install -y libgdal-dev
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# install python libraries
RUN pip3 install bidict==0.22.1
RUN pip3 install cffi==1.16.0
RUN pip3 install click==8.1.7
RUN pip3 install colorama==0.4.6
RUN pip3 install dnspython==2.5.0
RUN pip3 install eventlet==0.33.3
RUN pip3 install Flask==1.1.1
RUN pip3 install Flask-SocketIO==4.1.0
RUN pip3 install gevent==21.1.2
RUN pip3 install gevent-websocket==0.10.1
RUN pip3 install greenlet==1.0.0
RUN pip3 install h11==0.14.0
RUN pip3 install itsdangerous==2.0.1
RUN pip3 install Jinja2==3.0.3
RUN pip3 install MarkupSafe==2.1.4
RUN pip3 install numpy==1.24.4
RUN pip3 install opencv-contrib-python==4.9.0.80
RUN pip3 install pillow==10.2.0
RUN pip3 install pip==23.3.1
RUN pip3 install pycparser==2.21
RUN pip3 install python-engineio==3.13.0
RUN pip3 install python-socketio==4.2.0
RUN pip3 install setuptools==68.2.2
RUN pip3 install simple-websocket==1.0.0
RUN pip3 install six==1.16.0
RUN pip3 install Werkzeug==2.0.3
RUN pip3 install wheel==0.41.2
RUN pip3 install wsproto==1.2.0
RUN pip3 install zope.event==5.0
RUN pip3 install zope.interface==6.1
RUN pip3 install requests

# Copy over AutoDRIVE API
COPY AutoDRIVE_API ./AutoDRIVE_API

# Expose port
EXPOSE 4567

# Launch command here or in the kubernetes deployment
# CMD ["python /AutoDRIVE_API/rzr_aeb.py"]
