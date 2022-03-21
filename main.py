from nft_generator import AmazingAstronaut
from image_mappings import PATH_TO_GENERATED_FOLDER
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class NFT(BaseModel):
    background: str
    alien: str
    astronaut: str
    

@app.post("/mint")
async def create_item(nft: NFT):
    nft = AmazingAstronaut(nft.background, nft.alien, nft.astronaut)
    nft.generate_image_from_attributes()
    nft.generate_metadata()
    nft.upload_metadata_to_ipfs()
    etherscan_link, rarible_link = nft.mint_nft()
    return {
        "message": "NFT Mint was successful", 
        "etherscan_link": etherscan_link,
        "rarible_link": rarible_link
        }
