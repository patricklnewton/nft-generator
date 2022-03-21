from image_mappings import (
    BACKGROUNDS, 
    ALIENS, 
    ASTRONAUTS, 
    PATH_TO_GENERATED_FOLDER, 
    PATH_TO_ABI,
    IPFS_ID,
    IPFS_SECRET,
    IPFS_ENDPOINT,
    PRIVATE_KEY,
    PUBLIC_KEY,
    CONTRACT_ADDRESS,
    API_URL,
    )
from PIL import Image
import requests
import json
import logging
import os
from web3 import Web3

logging.basicConfig(level = logging.INFO)

class AmazingAstronaut:
    def __init__(self, background, alien, astronaut):
        self.background = background
        self.alien = alien
        self.astronaut = astronaut
        self.ipfs_image_hash = ''
        self.metadata = {}
        self.ipfs_metadata_hash = ''
        self.eth_json = {}
    
    def generate_image(self, background, alien, astronaut):
        new_background = Image.open(background)
        new_alien = Image.open(alien)
        new_astronaut = Image.open(astronaut)
        merge_layer = Image.alpha_composite(new_background, new_alien)
        final_img = Image.alpha_composite(merge_layer, new_astronaut)
        return final_img

    def generate_all_images(self):
        counter = 0
        for bg in BACKGROUNDS:
            for alien in ALIENS:
                for astro in ASTRONAUTS:
                    final_img = self.generate_image(BACKGROUNDS[bg], ALIENS[alien], ASTRONAUTS[astro])
                    final_img.save(f'{PATH_TO_GENERATED_FOLDER}/final_{counter}.png')
                    counter += 1

    def generate_image_from_attributes(self):
        if self.background in BACKGROUNDS and self.alien in ALIENS and self.astronaut in ASTRONAUTS:
            final_img = self.generate_image(BACKGROUNDS[self.background], ALIENS[self.alien], ASTRONAUTS[self.astronaut])
            final_img.save(f'{PATH_TO_GENERATED_FOLDER}/final_generated.png')
            logging.info('Image created.')
            self.upload_file_ipfs(f'{PATH_TO_GENERATED_FOLDER}/final_generated.png', False)
        else:
            logging.error('Unknown image assets.')
            quit()

    def upload_file_ipfs(self, file, isMetadata):
        files = {}
        try:
            f = open(file,'rb')
            files = {
                'file': open(file,'rb')
            }
        finally:
            f.close()
        
        if files:
            upload_response = requests.post(f'{IPFS_ENDPOINT}/add', files=files, auth=(IPFS_ID,IPFS_SECRET))
            res = json.loads(upload_response.text)
            if isMetadata:
                self.ipfs_metadata_hash = res['Hash']
            else:
                self.ipfs_image_hash = res['Hash']
        else:
            logging.error(FileNotFoundError)


    def generate_metadata(self):
        metadata = {
            'name': 'Amazing Astronauts',
            'description': 'To infinity and beyond!',
            'image': f'https://ipfs.io/ipfs/{self.ipfs_image_hash}',
            'attributes': [
                {
                    'trait_type': 'Background',
                    'value': self.background
                },
                {
                    'trait_type': 'Alien',
                    'value': self.alien
                },
                {
                    'trait_type': 'Astronaut',
                    'value': self.astronaut
                }
            ]
        }
        self.metadata = metadata
        logging.info('Metadata created.')
        self.upload_metadata_to_ipfs()

    def upload_metadata_to_ipfs(self):
        with open('nft_metadata.json', 'w') as outfile:
            json.dump(self.metadata, outfile)
    
        self.upload_file_ipfs(f'nft_metadata.json', True)

        if os.path.exists('nft_metadata.json'):
            os.remove('nft_metadata.json')
        else:
            logging.error(FileNotFoundError)
    
    def load_json(self, path_to_json):
        try:
            with open(path_to_json, "r") as config_file:
                conf = json.load(config_file)
                return conf

        except Exception as error:
            logging.error(error)
            raise TypeError("Invalid JSON file")

    def mint_nft(self):
        # grab contract ABI
        w3 = Web3(Web3.HTTPProvider(API_URL))
        abi = self.load_json(PATH_TO_ABI)["abi"]
        chain_id = 4
        
        #Connect to contract
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)  # The contract
        logging.info(f"checking if connected to infura...{w3.isConnected()}")

        #configure Metadata
        token_uri= f'https://ipfs.io/ipfs/{self.ipfs_metadata_hash}'
        nonce = w3.eth.get_transaction_count(PUBLIC_KEY)

        #create transaction
        mint_txn = contract.functions.mintNFT(PUBLIC_KEY, token_uri).buildTransaction(
            {
                "chainId": chain_id,
                "gas": 1000000,
                "gasPrice": w3.toWei("1", "gwei"),
                "nonce": nonce,
            }
        )

        #sign transaction
        signed_txn = w3.eth.account.sign_transaction(mint_txn, private_key=PRIVATE_KEY)
        w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        hash = w3.toHex(w3.keccak(signed_txn.rawTransaction))

        logging.info(f"mint txn hash: {hash} ")

        receipt = w3.eth.wait_for_transaction_receipt(hash)

        hex_tokenid = receipt["logs"][0]["topics"][3].hex()  # this is token id in hex

        # convert from hex to decimal
        tokenid = int(hex_tokenid, 16)
        logging.info(f"Token id: {tokenid} ")
        etherscan_link = f'https://rinkeby.etherscan.io/tx/{hash}'
        rarible_link = f'https://rinkeby.rarible.com/token/{CONTRACT_ADDRESS}:{tokenid}?tab=details'
        return etherscan_link, rarible_link
        

