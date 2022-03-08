# this is where we will test on a real chain
from brownie import network
import pytest
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    fund_with_link,
)
from scripts.deploy_lottery import deploy_lottery
import time


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    # Since we are on a real chain, we just need to wait for chainlink node to respond w random number
    # We will wait 1 minute
    time.sleep(60)
    # since we are the only acount to enter, we should be the winner and the lottery balance should return to 0
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
