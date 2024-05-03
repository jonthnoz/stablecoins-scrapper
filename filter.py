import json
import curses
from collections import Counter

def count_blockchains():
    blockchains = []
    with open('stablecoins.json', 'r') as file:
        data = json.load(file)
        for _, contracts in data.items():
            blockchains.extend(contracts['contracts'].keys())
            if 'main' in contracts['contracts'] and not 'Ethereum' in contracts['contracts'] and contracts['contracts']['main'].startswith('0x') and len(contracts['contracts']['main']) == 42:
                blockchains.append('Ethereum')
                blockchains.remove('main')
    return Counter(blockchains)

def filter_addresses(blockchain):
    filtered_addresses = {}
    with open('stablecoins.json', 'r') as file:
        data = json.load(file)
        if blockchain == 'main':
            for token, contracts in data.items():
                if 'main' in contracts['contracts'] and not (not 'Ethereum' in contracts['contracts'] and contracts['contracts']['main'].startswith('0x') and len(contracts['contracts']['main']) == 42):
                    filtered_addresses[token] = contracts['contracts']['main']
        elif blockchain == 'Ethereum':
            for token, contracts in data.items():
                if 'main' in contracts['contracts'] and not 'Ethereum' in contracts['contracts'] and contracts['contracts']['main'].startswith('0x') and len(contracts['contracts']['main']) == 42:
                    filtered_addresses[token] = contracts['contracts']['main']
                for token, contracts in data.items():
                    if blockchain in contracts['contracts']:
                        filtered_addresses[token] = contracts['contracts'][blockchain]
        else:
            for token, contracts in data.items():
                if blockchain in contracts['contracts']:
                    filtered_addresses[token] = contracts['contracts'][blockchain]

    return filtered_addresses

def save_addresses_to_file(blockchain, addresses):
    filename = f'{blockchain}_addresses.json'
    with open(filename, 'w') as file:
        json.dump(addresses, file, indent=4)
    return f'Addresses for {blockchain} saved to {filename}'

def select_blockchain(stdscr):
    blockchain_counts = count_blockchains().most_common()
    selected_index = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Choose a blockchain:")
        
        for i, (blockchain, count) in enumerate(blockchain_counts[selected_index:selected_index+3]):
            if i == 0:
                stdscr.addstr(i + 1, 0, f"> {blockchain} ({count} occurrences)")
            else:
                stdscr.addstr(i + 1, 0, f"  {blockchain} ({count} occurrences)")
        
        if len(blockchain_counts) > 3:
            stdscr.addstr(4, 0, "...")
        
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            selected_index = max(0, selected_index - 1)
        elif key == curses.KEY_DOWN:
            selected_index = min(len(blockchain_counts) - 1, selected_index + 1)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            chosen_blockchain = blockchain_counts[selected_index][0]
            addresses = filter_addresses(chosen_blockchain)
            if addresses:
                message = save_addresses_to_file(chosen_blockchain, addresses)
                stdscr.addstr(6, 0, message)
            else:
                stdscr.addstr(6, 0, f"No addresses found for {chosen_blockchain}")
            stdscr.getch()
            break

curses.wrapper(select_blockchain)
