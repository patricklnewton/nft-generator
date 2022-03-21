async function main() {
    const MyNFT = await ethers.getContractFactory("MyNFT");
    console.log('Deploying contract...');
    // Start deployment, returning a promise that resolves to a contract object
    const myNFT = await MyNFT.deploy();
    await myNFT.deployed();
    console.log("Contract deployed to address:", myNFT.address)
  }

const runMain = async () => {
    try {
        await main();
        process.exit(0);
    } catch (error) {
        console.log(error);
        process.exit(1);
    }
};

runMain();