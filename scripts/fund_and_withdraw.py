# import the required files into the script
from brownie import CrowdFund
from scripts.helpful_scripts import get_account

# function to interact with the contract and fund
def fund():
    crowd_fund = CrowdFund[-1]
    account = get_account()
    entrance_fee = crowd_fund.getEntranceFee()
    print(entrance_fee)
    print(f"the current entry fee is {entrance_fee}")
    print("funding")
    crowd_fund.fund({"from": account, "value": entrance_fee})

# function to interact with the contract and withdraw
def withdraw():
    crowd_fund = CrowdFund[-1]
    account = get_account()
    crowd_fund.withdraw({"from": account})

def main():
    fund()
    withdraw()
