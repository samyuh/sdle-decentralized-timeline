# SDLE Project - Group T3G13

### Group Members
1. Diogo Samuel Fernandes (up201806250@up.pt)
2. Hugo Guimarães  (up201806490@up.pt)
3. Paulo Ribeiro (up201806505@up.pt)
4. Telmo Baptista (up201806554@up.pt)

## Instructions

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
