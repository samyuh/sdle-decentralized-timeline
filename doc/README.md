# SDLE Project - Group T3G13

## Group Members
1. Diogo Samuel Fernandes (up201806250@up.pt)
2. Hugo Guimarães  (up201806490@up.pt)
3. Paulo Ribeiro (up201806505@up.pt)
4. Telmo Baptista (up201806554@up.pt)

## Description
Peer to peer Timeline built with Kademlia.

## Instructions

NOTE: Our project only works in the *Linux* environment due to the package simple_term_menu used for menus

1. Clone this repository:
```properties
git clone https://git.fe.up.pt/sdle/2021/t3/g13/proj2.git
```

2. From the root folder (`proj2`) run the following command to install the requirements:

- Create the Virtual Environment: `python -m venv env`
- Activate the Virtual Environment: `source env/bin/activate`
- Install the requirements: `pip install -r requirements.txt`

3. See the program usage using the following command:
```properties
python -m src -h
```

A detailed help message is printed, describing all the possible arguments.
The default ip is 127.0.0.1, the default port for the network is 8000 and the default port for the direct connections is 7000.

For example, running a bootstrap node with the default values would be achieved by the following command:
```properties
python -m src -init
```
Running a new user using the port 8003 for the network and the port 7003 for the direct connections between the peers is achieved using the following command:
```properties
python -m src -p 8003 -pl 7003
```

If values aren't specified, the default ones that are in the config.ini file will be used.

## Documents
A presentation and a video demonstration of this project can be found in the folder `doc`.

*Config.ini* specifications:
1. **[DEFAULT]** - Default values used in the communication with the network and between users
    - IP - Ip for the kademlia network communication 
    - PORT - Port for the kademlia network commucation 
    - LISTENING IP - Ip for the TCP communication between users
    - LISTENING PORT - Port for the TCP communication between users
2. **[BOOTSTRAP]** - Bootstrap node used to connect to the network through an existing peer
    - IP = 127.0.0.1 - Ip for the kademlia network communication of the bootstrap node
    - PORT = 8000 - Port for the kademlia network communication of the bootstrap node
3. **[MESSAGE_LIFESPAN]** - Maximum time a post stays in the timeline after its publishing date
    - ACTIVE = 1 - Boolean Value that indicates whether the message lifespan is being checked
    - YEARS = 0 - number of years to wait before post removal
    - MONTHS = 0 - number of months to wait before post removal
    - DAYS = 0 - number of days to wait before post removal
    - HOURS = 0 - number of hours to wait before post removal
    - MINUTES = 3 - number of minutes to wait before post removal
    - SECONDS = 0 - number of seconds to wait before post removal