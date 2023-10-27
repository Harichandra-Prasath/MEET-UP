# WebRTC Meet-Up Application

Welcome to the WebRTC Meet-Up application! This is a general-purpose meet application that allows multiple users to join a room, share their camera and microphone with other users, and engage in real-time communication using WebRTC. The backend is powered by Django Channels for signaling.

## Features
- Real-time video and audio communication through WebRTC API.
- Multiple users can join a room.
- Room chat for text communication.
- Utilizes Free TURN and STUN servers for establishing peer-to-peer connections.

## Installation

### Prerequisites
- Python 3.7+
- Django 2.0+
- Django Channels
- WebRTC-compatible web browsers (e.g., Chrome, Firefox)

### Steps
- git clone https://github.com/Harichandra-Prasath/MEET-UP/.
- cd webrtc-meetup.
- python -m venv venv.
- source venv/bin/activate.
- pip install -r requirements.txt.
- python manage.py migrate.
- python manage.py runserver.

### Usage
    Create a room or join an existing one.
    Share your camera and microphone.
    Enjoy real-time video and audio communication.
    Use the room chat for text communication.

### Replacing the TURN Servers
To ensure the privacy and performance of your WebRTC connections, it is recommended to replace the default TURN servers with your own. You can obtain free TURN servers from OpenRelay. 
### To do this:
- Visit OpenRelay and register for an account if you don't have one.
- Obtain your TURN server credentials (TURN server URL, username, and password).
- Replace the TURN server configuration in the application (room.js) under newpeertopeer connection

