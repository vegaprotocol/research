# Obfuscating or hiding order details on public order books

[![cryptography](https://img.shields.io/badge/-cryptography-%2382dd5a.svg?maxAge=25000)](https://github.com/vegaprotocol/research/labels/cryptography) [![market-microstructure](https://img.shields.io/badge/-market--microstructure-%237d63d3.svg?maxAge=25000)](https://github.com/vegaprotocol/research/labels/market-microstructure)

GitHub issue: [#4](https://github.com/vegaprotocol/research/issues/4)

## Description

Transparent order books are an area of ongoing research at Vega ([transparent-order-books](transparent-order-books.md)). One place where that may be challenging is for the implementation of order types such as stop loss and take profits that may be less useful or prone to gaming if the market is aware of the trigger level.
We have approaches such as probabilistic triggers, progressively revealed orders, etc. that may mitigate this, but there are also potential benefits to allowing order details to be hidden or partially hidden in some scenarios we are keen to novel methods if hiding orders' economic information in a distributed matching engine without compromising the functionality.

Examples could invole the application of zero knowledge proofs or homomorphic encryption techniques.
