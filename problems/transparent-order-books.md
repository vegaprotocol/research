# Impact of transparent order books

GitHub issue: [#3](https://github.com/vegaprotocol/research/issues/3)

## Description

Vega's initial design has a fully transparent order book, meaning order types like iceberg orders don't make sense and conditional orders like stop loss and take profit orders are fully visible to entire market.

We'd like to explore what this means in terms of competitive outcomes? Is the mere fact that the full transparency applies to everyone sufficient to dampen the gaming attacks that would otherwise result if this knowledge was asymmetric?