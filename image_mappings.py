import os
from dotenv import load_dotenv

load_dotenv()
IPFS_ID = os.getenv('IPFS_ID')
IPFS_SECRET = os.getenv('IPFS_SECRET')
IPFS_ENDPOINT = os.getenv('IPFS_ENDPOINT')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
PUBLIC_KEY = os.getenv('PUBLIC_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')
API_URL = os.getenv('API_URL')

file_path_to_assets = f'{os.path.dirname(os.path.abspath(__file__))}/assets'

file_locations = {
    'bg_sun' : f'{file_path_to_assets}/bg_sun.png',
    'bg_moon' : f'{file_path_to_assets}/bg_moon.png',
    'bg_planets': f'{file_path_to_assets}/bg_planets.png',
    'astro_red': f'{file_path_to_assets}/astro_red.png',
    'astro_blue': f'{file_path_to_assets}/astro_blue.png',
    'astro_white': f'{file_path_to_assets}/astro_white.png',
    'alien_green': f'{file_path_to_assets}/alien_green.png',
    'alien_red': f'{file_path_to_assets}/alien_red.png',
    'alien_purple': f'{file_path_to_assets}/alien_purple.png'
}

BACKGROUNDS = {
    'bg_sun' : f'{file_path_to_assets}/bg_sun.png',
    'bg_moon' : f'{file_path_to_assets}/bg_moon.png',
    'bg_planets': f'{file_path_to_assets}/bg_planets.png',
}

ASTRONAUTS = {
    'astro_red': f'{file_path_to_assets}/astro_red.png',
    'astro_blue': f'{file_path_to_assets}/astro_blue.png',
    'astro_white': f'{file_path_to_assets}/astro_white.png',
}

ALIENS = {
    'alien_green': f'{file_path_to_assets}/alien_green.png',
    'alien_red': f'{file_path_to_assets}/alien_red.png',
    'alien_purple': f'{file_path_to_assets}/alien_purple.png'
}

PATH_TO_GENERATED_FOLDER = f'{os.path.dirname(os.path.abspath(__file__))}/generated'
PATH_TO_ABI = f'{os.path.dirname(os.path.abspath(__file__))}/smart-contract/artifacts/contracts/MyNFT.sol/MyNFT.json'


