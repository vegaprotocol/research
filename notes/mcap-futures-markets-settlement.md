# Research note: settling market capitalisation pre-launch token futures

This note is a response to community interest in creating futures markets on the market capitalisation of various tokens prior to token launch, aka "MCAP futures" or "MCAP markets".

It describes one way to define when and how to settle such markets given the broad possible number of outcomes and the lack of ahead-of-time certainty as to whether a token will launch and if it does, what the market capitalisation will be at launch.

The approach is based on [the methodology we developed for settling "points markets"](https://github.com/vegaprotocol/research/blob/master/notes/points-markets-settlement.md). Both are modelled on Credit Default Swaps (CDS) which are derivatives that are valued based on the probability of a company defaulting. Payouts are triggered when a “credit event” occurs, as defined by a set of explicit rules. Analogously, we define the concept of an “token launch” that can be similarly used to determine when and at what value to settle MCAP futures.


## Conceptual overview

Conceptually, we need to define four things to enable fair and orderly settlement of an mcap futures market:

1. The ***fraction of mcap** that will correspond to one futures contract on the Vega chain. This fraction of mcap can be e.g. 1e-9 for a project who's anticipated market capitalisation is 1 billion USDT (so 1e9 USDT) at launch. Such contract would be expected to trade around 1 USDT.  

2. The conditions under which the ***token launch*** has been deemed to have occurred, and the market may settle.

3. The ***MCAP Valuation Algorithm*** for calculating the relevant market capitalisation for settlement purposes.

4. The ***futures contract settlement price***  is defined as soon as the MCAP valuation algorithm has provided an accepted answer hence the value of 1 futures contract on the vega chain can be obtained.

 

## Detailed definition

### Terms

These terms have specific meanings in the text below

*token*
: Any asset issued by a protocol or company that has utility for the project / company and exists on any public blockchain (a typical example would be an ERC20 on Ethereum). 

*termination date/time*
: The time at which trading on the vega futures market should stop as a result  ***MCAP Valuation Algorithm*** providing an accepted value.


### Variables

The following terms (with suggested values in brackets) used in the definitions refer to quantities or other parameters that affect the specifics of the product. They may be varied to suit each individual use case.

`Base Asset` (USDT)
: The asset in which market capitalisation of the token is considered.

`Inclusivity Threshold` (40.00%)
: The percentage of tokens freely circulating out of a total number of project tokens.

`Expiry Date/Time` (optional)
: *If specified* the market would settle at a price of zero at the expiry date/time if no accepted value has been produced by the ***MCAP Valuation Algorithm*** on or before the specified date and time.

`Liquidity Threshold` (0.05% = 5bp = 0.0005)
: The fraction of total number of tokens that must available to be bought *and* sold in the market (across valid exchanges defined below) within `valid slippage` (%) of the current price per point.

`Valid Slippage` (20.00%)
: The range around the current market price at which available bids are deemed to constitute ‘liquidity’ for the purpose of the ***MCAP Valuation Algorithm***.

`Minimum Trading Window` (48 hours)
: The minimum amount of cumulative time over which a market meeting the liquidity and slippage thresholds must exist to trigger a successful ***MCAP Valuation Algorithm*** calculation.

`Valid Exchanges`
: A list of exchanges on which the listing of the token would count as valid for measurement of price. These may include a list of major centralised exchanges such as Binance, ByBit or Coinbase or significant decentralised spot exchanges on the chains where the token is likely to be launched (Uniswap for Ethereum, Osmosis for Cosmos etc.).


### MCAP Valuation Algorithm

Once the token has launched and has been trading for `Minimum Trading Window` with sufficient `Liquidity Threshold` the valuation algorithm will calculate the MCAP as:
```
MCAP = TWAP x total_supply,
```
where

- `TWAP` is the time-weighted average price of the token, over the minimum trading window and
- `total_supply` the total number of tokens issued (whether circulating or not). 

The settlement price is then obtained as the `fraction of mcap for 1 futures contract x MCAP` E.g. if the fraction of mcap for 1 futures contract is 1e-9 and the valuation algorithm delivers 2.3e10 as the relevant market capitalisation then the settlement price is `2.3e10 x 1e-9 = 23 USDT`. 


# Appendix I: Settling with UMA Optimistic Oracle v3

In addition to this research note, the Vega engineering team have prepared a [template Solidity smart contract](https://github.com/vegaprotocol/uma-oracle-contract-template) that can be customised as needed and deployed in order to settle a market using the approach outlined in this note.

The README file in that repository contains more details on its technical use and deployment. In order to use the contract, this abstract note needs to be turned into a more specific settlement specification that can be followed by users of the UMA Optimistic Oracle protocol. Suggested steps to do so are described below.

1. Decide on the values for the variables listed above.

2. Copy the text above under "Detailed definition", replacing the `variable markers` (i.e. variable names using inline code formatting) with your chosen values. Remove the variables section. (Alternatively, define the variables clearly in the variables section and leave it in place.)

3. Edit the text, removing any parts that are not relevant for the given market and/or chosen variable values. Add an introduction and ensure it is as clear as possible exactly how to settle the market. Remember this research note provides a generic approach but it may be able to be simplified for a given case. **If this is not clear, or is ambiguous, then the settlement of the market may be at risk, so pay attention at this stage to enure the text for your specific use case is worded as well as possible.**

4. Add Vega specifics like the required decimal places and/or integer conversions, the asset the price should be in (e.g. USDT, USDC, etc.), which should be the settlement asset of the market, not fiat USD nor the bond currency of the UMA oracle (unless this happens to be the same). 

5. Upload the text somewhere immutable like IPFS.

6. Deploy the contract and create the Vega market, referencing both the contract address (and chain) and the IPFS link to the text in the Vega market specification. Note that the text can be changed by governance on Vega by voting through a new IPFS link as a change to the market specification.
