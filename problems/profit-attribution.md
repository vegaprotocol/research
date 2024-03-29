# Profit attribution on blockchain

[![markets](https://img.shields.io/badge/-markets-%23f9efa9.svg?maxAge=25000)](https://github.com/vegaprotocol/research/labels/markets) [![mechanism-design](https://img.shields.io/badge/-mechanism--design-%23e0d61f.svg?maxAge=25000)](https://github.com/vegaprotocol/research/labels/mechanism-design)

GitHub issue: [#13](https://github.com/vegaprotocol/research/issues/13)

## Description

In many blockchain settings that go beyond proof-of-work type currencies like Bitcoin, developers are proposing to run profitable applications on top of either proof-of-work or proof of stake networks.

To run the application operators need capital, have costs (you can treat capital as cost perhaps) but can collect fees. However they need node operators to run the infrastructure. The node operators don't collect fees but should be rewarded by the application layer sufficiently. Clearly they have costs (capital, electricity, bandwidth) and if the reward is too low the application providers will end up with a network that either doesn't run, or is unstable or faces other problems.

Develop a framework (using stakeholder voting, or principal-agent setup) to model this situation and conclude something about an appropriate split of revenue (e.g. as a function of costs).
