# import the required files into the script
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_crowd_fund
from brownie import network, accounts, exceptions
import pytest

# tests should always pass on brownie ganache chain with mocks
# tests should always pass on testnet (only for integration settings)
# tests on brownie mainnet-fork and custom mainnet-fork are optional
# testing on a local ganache chain is not require but good for tinkering

def test_can_fund_and_withdraw():
    account = get_account
    crowd_fund = deploy_crowd_fund()
    entrance_fee = crowd_fund.getEntranceFee() + 100
    tx = crowd_fund.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert crowd_fund.addressToAmount(account.address) == entrance_fee
    tx2 = crowd_fund.withdraw({"from": account})
    tx2.wait(1)
    assert crowd_fund.addressToAmount(account.address) == 0

# skip the test if on the local network
def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("it is only for local testing")
    crowd_fund = deploy_crowd_fund()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        crowd_fund.withdraw({"from": bad_actor})
