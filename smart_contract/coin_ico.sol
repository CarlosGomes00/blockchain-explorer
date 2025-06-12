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
    uint public coin_bought = 0; 

    //Matching funcs
    mapping(address => uint) equity_coin;
    mapping (address => uint) equity_usd;

    //Checks if the investor can buy coin
    modifier can_buy_coin(uint usd_invested){
        require(usd_invested * usd_to_coin + coin_bought <= max_coin, "Insufficient balance");
        _;
    }
}

