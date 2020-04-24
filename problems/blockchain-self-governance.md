# Flexible & self-governing architecture

GitHub issue: [#1](https://github.com/vegaprotocol/research/issues/1)

## Description

### Overview

We are designing modular architecture to allow markets high flexibility to choose their configuration and blockchain behaviour, updates to be efficiently handled on-chain, and dynamic adaption to the network and environmental factors.

### Details

While the progression of a blockchain is usually well distributed among a number of validators,
the factors that cover governance - setting various operational parameters, performing updates in the code or the algorithms, etc - are often far less distributed. To make things worse, many decisions cannot be voted on by the same structures the validators use - for example, validators might have an economic interest in keeping other validators out, and thus should not be responsible for membership decisions. Another issue is voting competence - some stakeholders may be in just as an investment and have little motivation to obtain all the knowledge needed for a competent vote. Other decisions that a self-governing blockchain needs to be able to make include for example

- The reward scheme: how are validators paied in a way that keeps them motivated to do their job,
without increasing the transaction cost or motivating validators to be too big or too small ?
How can we avoid validators to do a good job and not try to get away getting paid for the minimum
work possible? (see also: [#12](beyond-proof-of-stake.md))
- Validator Membership: How can we keep a validator set of validators that have sufficient performance,
are well distributed, and can't end up having a monopoly that can dictate prices ?
- Code updates: When and how is the implementation changed in a way that there is no single entity
dictating the code and while avoiding hard forks ?
- Runntime parameters, such as timeouts

## Features

- Modular design with on-the-fly exchangeable components
- Self-governing update & parameter

**Research Question:** For above questions (as well as more that are still identified), propose a voting setting in which all decisions are made by voters that have both the competency and the interest to make decisions that are in the best interest of a robust and well decentralised blockchain. (It might be a good starting point to give a good definition what that actually is).
