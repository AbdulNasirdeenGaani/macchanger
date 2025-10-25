import subprocess
import optparse


def get_arguments():
    parse = optparse.OptionParser()
    parse.add_option("-i", "--interface", dest="interface", help="Network interface to change its MAC address")
    parse.add_option("-m", "--mac", dest="new_mac", help="New MAC address to assign to the network interface")

    if not parse.parse_args()[0].interface:
        parse.error("[-] Please specify an interface, use --help for more info.")
    if not parse.parse_args()[0].new_mac:
        parse.error("[-] Please specify a new MAC address, use --help for more info.")
    return parse.parse_args()


def change_mac(interface, new_mac):
    """
    Change the MAC address of a network interface.

    :param interface: The network interface to change (e.g., 'eth0', 'wlan0').
    :param new_mac: The new MAC address to assign to the interface.
    :call on terminal with 'sudo python3 macchanger.py -i <interface> -m <new_mac>' OR
    :sudo python3 macchanger.py --interface <interface> --mac <new_mac>
    """
    try:
        # Bring the interface down
        subprocess.run(['sudo', 'ifconfig', interface, 'down'], check=True)
        
        # Change the MAC address
        subprocess.run(['sudo', 'ifconfig', interface, 'hw', 'ether', new_mac], check=True)
        
        # Bring the interface back up
        subprocess.run(['sudo', 'ifconfig', interface, 'up'], check=True)
        
        print(f"MAC address for {interface} changed to {new_mac}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def print_new_mac(interface):
    ifconfig = subprocess.check_output(['ifconfig', interface]).decode('utf-8')
    for line in ifconfig.split('\n'):
        if 'ether' in line:
            print(f"New MAC address: {line.strip().split(' ')[1]}")

if __name__ == "__main__":
    (options, arguments) = get_arguments()
    change_mac(options.interface, options.new_mac)
    print_new_mac(options.interface)    # Change the MAC address of a network interface.