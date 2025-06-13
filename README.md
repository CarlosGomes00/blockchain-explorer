# blockchain-explorer

# Exploring the blockchain

This repository contains a simple yet functional blockchain implementation written in Python. It serves as a practical sandbox to help me understand the inner workings of blockchain technology, smart contracts and decentralized networks work under the hood.

## What's in the repository?

- A fully functional blockchain created from scratch
- Mining mechanism using Proof of Work (PoW)
- Flask-based REST API to interact with the blockchain
- Transaction handling system
- Node networking with consensus protocol (for syncing between nodes - The coin5001, coin5002 and coin5003 files represent different nodes)

Available API endpoints:
  -- GET `/mine_block`: mines a new block
  -- GET `/get_chain`: returns the full blockchain
  -- GET `/is_valid`: checks if the blockchain is valid
  -- POST `/add_transaction`: Adds a new transaction
  -- POST `/connect_node`: Connects the different nodes
  -- GET `/replace_chain`: Updates outdated nodes

- It also has templates (relating to transactions and connections between nodes) in json format, available to be added to Postman
- A work-in-progress Solidity Smart Contract for an Initial Coin Offering (ICO). This contract aims to simulate a basic token sale mechanism on a blockchain-like environment.

## Why this project?

In recent years, my curiosity about cryptocurrencies and their market has grown significantly. 
To avoid relying my investments solely on technical analysis of price charts and to become more familiar with the underlying technologies, I decided to take a mini-course to deepen my knowledge of the technologies that power cryptocurrencies.

