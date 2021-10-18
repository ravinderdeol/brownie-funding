# import the required files into the script
from brownie import CrowdFund, MockV3Aggregator, network, config
from scripts.helpful_scripts import (deploy_mocks, get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS)

# function to deploy the contract
def deploy_crowd_fund():
    account = get_account()

    # if on persistent network (rinkeby) use address else deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        feed_address = MockV3Aggregator[-1].address
    
    # from key is required when deploying to a chain to make a state change
    # programatically verify smart contract on etherscan using an api
    crowd_fund = CrowdFund.deploy(
        feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"))
   
    print(f"contract deployed to {crowd_fund.address}")
    return crowd_fund

def main():
    deploy_crowd_fund()
