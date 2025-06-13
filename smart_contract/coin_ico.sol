// Coin ICO

// SPDX-License-Identifier: MIT
//Compiler version
pragma solidity ^0.4.11

contract coin_ico {
    //Max number of available coins
    uint public max_coin = 1000000;

    //Coin cotation against dollar
    uint public usd_to_coin = 1000;

    //Coin bought by investors
    uint public total_coin_bought = 0; 

    //Matching funcs
    mapping(address => uint) equity_coin;
    mapping (address => uint) equity_usd;

    //Checks if the investor can buy coin
    modifier can_buy_coin(uint usd_invested){
        require(usd_invested * usd_to_coin + total_coin_bought <= max_coin, "Insufficient balance");
        _;
    }

    //Return the invested value in coin
    function equity_in_coin(address investor) external constant returns(uint){
        return equity_coin[investor];
    } 

    //Return the invested value in usd
    function equity_in_usd(address investor) external constant returns(uint){
        return equity_usd[investor];
    } 

    //Coin purchase
    function buy_coin(address investor, uint usd_invested) external 
    can_buy_coin(usd_invested) {
        uint coin_bought = usd_invested * usd_to_coin;
        equity_coin[investor] += coin_bought;
        equity_usd[investor] += usd_invested;
        total_coin_bought += coin_bought;
    }

    //Coin sell
    function sell_coin(address invester, uint coin_sold) external {
        require( equity_coin[invester] >= coin_sold, 'Not enough coins to sell');
        uint usd_to_return = coin_sold / usd_to_coin;
        equity_coin[investor] -= coin_sold;
        require(equity_usd[investor] >= usd_to_return, 'USD balance underflow error');
        equity_usd[investor] -= usd_to_return;
        require(total_coin_bought >= coin_sold, 'Total coins bought underflow error');
        total_coin_bought -= coin_sold;
    }
}

