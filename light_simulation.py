#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time
import sys
import signal
import os
from datetime import datetime

# MQTT Broker details
MQTT_BROKER = "157.173.101.159"  # Replace with your broker's IP or hostname
MQTT_PORT = 1883  # Standard MQTT port
MQTT_TOPIC = "/student_group/light_control"  # Topic to subscribe to

# Light state
light_state = "UNKNOWN"

# ANSI color codes for terminal output
class Colors:
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    """Print a nice header for the simulator"""
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'IoT Light Simulator'.center(60)}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'ESP8266 Simulation'.center(60)}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"\n{Colors.BOLD}MQTT Broker:{Colors.ENDC} {MQTT_BROKER}")
    print(f"{Colors.BOLD}MQTT Topic:{Colors.ENDC} {MQTT_TOPIC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'-'*60}{Colors.ENDC}\n")

def on_connect(client, userdata, flags, rc):
    """Callback for when the client connects to the broker"""
    if rc == 0:
        print(f"{Colors.GREEN}✓ Connected to MQTT broker{Colors.ENDC}")
        print(f"{Colors.BLUE}Subscribing to topic: {MQTT_TOPIC}{Colors.ENDC}")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"{Colors.RED}✗ Failed to connect, return code: {rc}{Colors.ENDC}")

def on_message(client, userdata, msg):
    """Callback for when a message is received"""
    global light_state
    payload = msg.payload.decode('utf-8')
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    if payload == "ON":
        light_state = "ON"
        print(f"{timestamp} | {Colors.YELLOW}💡 Light is TURNED ON{Colors.ENDC}")
    elif payload == "OFF":
        light_state = "OFF"
        print(f"{timestamp} | {Colors.RED}💡 Light is TURNED OFF{Colors.ENDC}")
    else:
        print(f"{timestamp} | {Colors.BLUE}Received unknown command: {payload}{Colors.ENDC}")
    
    print_status()

def print_status():
    """Print the current status of the light"""
    print(f"\n{Colors.BOLD}Current Status:{Colors.ENDC}", end=" ")
    if light_state == "ON":
        print(f"{Colors.YELLOW}💡 ON{Colors.ENDC}")
    elif light_state == "OFF":
        print(f"{Colors.RED}💡 OFF{Colors.ENDC}")
    else:
        print(f"{Colors.BLUE}💡 UNKNOWN{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'-'*60}{Colors.ENDC}")

def on_disconnect(client, userdata, rc):
    """Callback for when the client disconnects from the broker"""
    if rc != 0:
        print(f"{Colors.RED}✗ Unexpected disconnection. Attempting to reconnect...{Colors.ENDC}")

def signal_handler(sig, frame):
    """Handle keyboard interrupt"""
    print(f"\n{Colors.BLUE}Disconnecting from MQTT broker...{Colors.ENDC}")
    client.disconnect()
    print(f"{Colors.GREEN}Goodbye!{Colors.ENDC}")
    sys.exit(0)

def main():
    """Main function"""
    global client
    
    # Set up signal handler for graceful exit
    signal.signal(signal.SIGINT, signal_handler)
    
    # Print header
    print_header()
    
    # Create MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    
    # Connect to broker
    print(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}...")
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
    except Exception as e:
        print(f"{Colors.RED}✗ Failed to connect: {e}{Colors.ENDC}")
        sys.exit(1)
    
    # Start the loop
    print(f"{Colors.GREEN}Starting MQTT loop...{Colors.ENDC}")
    print(f"{Colors.BLUE}Press Ctrl+C to exit{Colors.ENDC}")
    print_status()
    
    # Keep the script running
    client.loop_forever()

if __name__ == "__main__":
    main()