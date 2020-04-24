# Liquidity markets

GitHub issue: [#11](https://github.com/vegaprotocol/research/issues/11)

## Description

We have just finsished a paper (we will add here when published) but this is the abstract, meanwhile:

> Exchanges and other trading venues must be able to reliably offer sufficient liquidity to meet traders' demand, and, in turn, benefit from higher revenue and faster growth when markets are liquid. Traders enjoy lower volatility, tighter spreads, and more efficient pricing in liquid markets. A key problem for exchanges is how to attract liquidity providers and retain their support in all market conditions. This is commonly approached through individual business agreements with market makers whereby a bespoke contract is negotiated for specific obligations and rewards. Such approaches require a central intermediary that profits from liquidity provision to administer, and typically fail to align the incentives of exchanges and liquidity providers as markets grow. This is costly, slow, and scalability is limited by the exchange’s resources, contacts, and expertise.
>
> This paper develops mechanisms for creating open, automated and scalable {\em liquidity markets}. We describe more formal methods to quantify liquidity and discuss various approaches to determine its price. In so doing, we introduce a novel way to structure liquidity commitments, along with a mechanism based on a financial bond with penalties for under-provision to maximise market makers’ adherence to their obligations. We also investigate mechanisms to allocate rewards derived from trading fees between market makers, so as to incentivise desirable-but-risky behaviours such as market creation and early commitment of liquidity. We complement this work with several agent based simulations exploring the proposed mechanisms.

We are interested in extending this research, including building out the agent based simulations to accommodate more complex pricing and liquidity provision assumptions.
