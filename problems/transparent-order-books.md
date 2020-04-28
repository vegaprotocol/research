# Impact of transparent order books

[![game-theory](https://img.shields.io/badge/-game--theory-%238af7ec.svg?maxAge=25000)](https://github.com/vegaprotocol/research/labels/game-theory) [![market-microstructure](https://img.shields.io/badge/-market--microstructure-%237d63d3.svg?maxAge=25000)](https://github.com/vegaprotocol/research/labels/market-microstructure)
GitHub issue: [#3](https://github.com/vegaprotocol/research/issues/3)

## Description

Vega's initial design has a fully transparent order book, meaning order types like iceberg orders don't make sense and conditional orders like stop loss and take profit orders are fully visible to entire market.

We'd like to explore what this means in terms of competitive outcomes? Is the mere fact that the full transparency applies to everyone sufficient to dampen the gaming attacks that would otherwise result if this knowledge was asymmetric?
