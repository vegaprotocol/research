# Financial risk management in a decentralised setting

[![quantitative-finance](https://img.shields.io/badge/-quantitative--finance-%23c6e861.svg?maxAge=25000)](https://github.com/vegaprotocol/research/labels/quantitative-finance) [![mechanism-design](https://img.shields.io/badge/-mechanism--design-%23e0d61f.svg?maxAge=25000)](https://github.com/vegaprotocol/research/labels/mechanism-design)

GitHub issue: [#14](https://github.com/vegaprotocol/research/issues/14)

## Description

When dealing with financial products it is import to accurately estimate risks involved. This requirement is even more pressing in the case of derivatives. While there are many potential sources of risk, some of which are quite esoteric and difficult to quantify, market risk is often the one that is considered the most.

For the purposes of this problem we can define market risk as distribution of prices for a given market at a fixed point in the future. Any form of risk management requires taking a view on what that future price distribution may be.

In a centralised setting it would be chosen by single entity according to well defined set of rules and regulations. In a decentralised setting anyone should be able to put forward their view on it.

As this process is non-trivial and has high potential consequences for the market an adequate incentive scheme must be put in place to encourage views that are most likely to be accurate (and are not deliberately manipulated to extract gains from the market by acting as a market-participant). Downplaying potential downside and exaggerating upside of future market moves might encourage excessive risk-taking and in turn a series of defaults possibly followed by a market crash. An overly conservative prognosis might reduce market activity which is an undesirable outcome from the point of view of the exchange.

Research problems:

- Devise a scheme encouraging agents to put forward accurate estimate of the future price distribution.
- Consider a multi-agent extension of the problem where risk management actions are taken based an amalgamation of multiple views of the future price distribution.

References / reading list:

- Our whitepaper, chapters 6.1 & 6.2 - [https://vega.xyz/papers/vega-protocol-whitepaper.pdf](https://vega.xyz/papers/vega-protocol-whitepaper.pdf)
- [Incentives for Model Calibration on Decentralized Derivatives Exchanges: Consensus in Continuum](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3534272)
- Article from FT on how clearing houses work (risk management in a centralised setting): [https://www.ft.com/content/01596fde-b805-11e8-b3ef-799c8613f4a1](https://www.ft.com/content/01596fde-b805-11e8-b3ef-799c8613f4a1)
- Martin Hugh's lecture notes, Lecture 6: Model Risk - [http://www.columbia.edu/~mh2078/QRM/ModelRisk.pdf](http://www.columbia.edu/~mh2078/QRM/ModelRisk.pdf) - no need to go deep into the details, more for overview of importance of model specification and calibration.
