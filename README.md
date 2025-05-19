# MSN2 - P2P Chat Application

A simple peer-to-peer chat application with basic encryption built in Python. This application allows multiple users to connect and chat directly with each other.

## Features

- P2P communication
- Basic Caesar cipher encryption
- Multiple simultaneous connections
- Command-line interface
- Dynamic peer connection

## Requirements

- Python 3.6+
- No additional packages required

## Installation

1. Clone or download the repository
2. Navigate to the project directory
```bash
cd path/to/project
```

## Usage

### Basic Start
To start the application, you need to specify a port to listen on:
```bash
python p2pchat.py -p 5000
```

### Connect to Peers
You can connect to existing peers when starting the application:
```bash
# Connect to one peer
python p2pchat.py -p 5000 -c 192.168.1.100:5001

# Connect to multiple peers
python p2pchat.py -p 5000 -c 192.168.1.100:5001 192.168.1.101:5002
```

### Commands
While running, the following commands are available:

- `/connect host:port` - Connect to a new peer
- `/exit` - Close all connections and exit the program

### Example Scenarios

#### Scenario 1: Two Users on Same Network
User A:
```bash
python p2pchat.py -p 5000
```

User B:
```bash
python p2pchat.py -p 5001 -c localhost:5000
```

#### Scenario 2: Multiple Users
User A (first user):
```bash
python p2pchat.py -p 5000
```

User B (connecting to A):
```bash
python p2pchat.py -p 5001 -c 192.168.1.100:5000
```

User C (connecting to both A and B):
```bash
python p2pchat.py -p 5002 -c 192.168.1.100:5000 192.168.1.101:5001
```

## Message Format
Messages appear in the following format:
```
[peer_ip:port]> message
```

## Security Note
This application uses a basic Caesar cipher for encryption. This is NOT secure for sensitive communications and should only be used for educational purposes.

## Troubleshooting

1. **Connection Failed**
   - Verify the port is not in use
   - Check if firewall is blocking connections
   - Ensure IP address is correct

2. **Can't Exit Program**
   - Use `/exit` command
   - Press Ctrl+C if unresponsive

## Contributing
Feel free to submit issues and enhancement requests!

## License
This project is open source and available under the MIT License.