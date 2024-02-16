# Research note: settling points airdrop futures

This note is a response to community interest in creating futures markets on the value of “points” being awarded by various protocols prior to token launch and in anticipation of an airdrop.

It describes one way to define when and how to settle such markets given the broad possible number of outcomes and the lack of ahead-of-time certainty as to what (if anything) points holders will receive, when they will receive it, and even whether all points will have the same future value.

The approach is modelled on Credit Default Swaps (CDS) which are derivatives that are valued based on the probability of a company defaulting. Payouts are triggered when a “credit event” occurs, as defined by a set of explicit rules. Analogously, we define the concept of an “airdrop event” that can be similarly used to determine when and at what value to settle points futures.


## Conceptual overview

Conceptually, we define three things to enable fair and orderly settlement of a points futures market:

1. The conditions under which the ***Airdrop Event*** has been deemed to have occurred, and the market may settle.

2. The rules for when to halt trading prior to settlement (to ensure orderly settlement while the final price is calculated and verified) due to an ***Imminent Airdrop Event***.

3. The ***Valuation Algorithm*** for calculating the *mean conversion rate* that defines the value of one point at settlement.


## Detailed definitions

### Terms

These terms have specific meanings in the text below

*points*
: Any pseudo-asset issued by a protocol or company (e.g. for activity or engagement with a project/protocol/product) that is not fungible or directly tradable. For example, points issued by protocols/networks like Hyperliquid, EigenLayer as well as loyalty points such as those issued by airlines and supermarkets.

*conversion*
: Any process by which some or all *points* become fungible assets such as protocol tokens or stablecoins, or become definitively valueless (e.g. a user/key’s balance is cleared). *Conversion* is considered to be complete when it is possible to value the points involved in the `Base Asset` (i.e. if points convert to a token with no market price, conversion may not be complete).

*mean conversion rate*
: The average rate in terms of the `Base Asset` at which each point involved in an *Airdrop Event* underwent *conversion*.

*termination date/time*
: The time at which trading on the market should stop as a result of an ***Imminent Airdrop Event***.


### Variables

The following terms (with suggested values in brackets) used in the definitions refer to quantities or other parameters that affect the specifics of the product. They may be varied to suit each individual use case.

`Base Asset` (USDT)
: The asset in which *points* that have undergone `conversion` are valued.

`Inclusivity Threshold` (40.00%)
: The percentage of issued points that must be eligible for the conversion

`Liquidity Threshold` (5.00%)
: The percentage of issued points that must be met by the bid depth (quantity of resting buy orders or points otherwise able to be sold) in the market within `valid slippage` (%) of the current price per point.

`Valid Slippage` (20.00%)
: The range around the current market price at which available bids are deemed to constitute ‘liquidity’ for the purpose of an ***Airdrop Event*** in which points have become tradable.

`Minimum Trading Window` (48 hours)
: The minimum amount of cumulative time over which a market meeting the liquidity and slippage thresholds must exist to trigger an ***Airdrop Event***.

`Early Termination Period` (24 hours)
: The amount of time before a scheduled ***Airdrop Announcement***

`Valid Exchanges`
: A list of exchanges on which the listing of a token/point would count as valid for measurement of price. These may include a list of major centralised exchanges such as Binance, ByBit or Coinbase or significant decentralised spot exchanges on the chains where the token is likely to be launched (Uniswap for Ethereum, Osmosis for Cosmos etc.).


### Airdrop Event

An ***Airdrop Event*** is deemed to have occurred when one or more of the following conditions is satisfied:

1. At least `Inclusivity Threshold` (%) of all issued *points* have undergone *conversion* (defined above) since the inception of the points programme.

2. It is no longer possible for *conversion* to happen, for example if the protocol ceases operation. (In this case the *mean conversion rate* will be zero.)

3. Points become freely tradable by the majority of points holders to the extent that a current market price per point exists and the cumulative historic trading volume plus the available liquidity within `Valid Slippage` of the current market price is at least `Liquidity Threshold` (%) of the total number of issued points for a (not necessarily contiguous) period of no less than `Minimum Trading Window`.  

Note: adjustments to points balances such as normal or reverse splits (1 point becomes, 2 points, 10 points, 100 points, 0.5 points, 0.1 points, etc.), multiplying some users points by some value, etc. etc. do not constitute an *Airdrop Event* and simply impact the market price of a point as an issuance of new points would.

Once an ***Airdrop Event*** has occurred and all input to the ***Valuation Algorithm*** is available, the *mean conversion rate* is calculated and the market will be settled. 


### Imminent Airdrop Event

An ***Imminent Airdrop Event*** will occur following any official confirmation (including implied confirmation as a result of the action happening before any official communication) of a future *conversion*, listing, or other action that would constitute an ***Airdrop Event***. 

For an announcement or action to trigger an ***Imminent Airdrop Event*** it must originate from or be endorsed as truthful and accurate by the project or another entity with sufficient control to initiate an ***Airdrop Event***.

The *termination date/time* shall be `Early Termination Period` before any announcement in which the specifics of the ***Airdrop Event*** that are required by the ***Valuation Algorithm*** are confirmed.

In the event that the data required by the ***Valuation Algorithm*** are available with less than `Early Termination Period` of notice (either due to an unannounced ***Airdrop Event*** or listing, or due to a short period between announcement and implementation), the *termination date/time* will be the current date/time (i.e. termination is immediate).

Note that due to the specifics of oracle protocols, etc. there may be a delay between the conditions for triggering an ***Imminent Airdrop Event*** and the data reaching a market on-chain and the cessation of trading.


### Valuation Algorithm

Once an airdrop event has been declared, it is necessary to calculate a value per point in order to settle the market. In some cases this may be possible immediately, and in others more information may be required even once the Airdrop Event has been triggered.

In cases where points have undergone *conversion* as defined above, or where *conversion* is no longer possible (***Airdrop Event*** cases 1 & 2):

- The *mean conversion rate* is the total value in the `Base Asset` distributed to *points* holders (which may be zero in some cases) divided by the total number of *points* that have either undergone *conversion* or been destroyed / become valueless.


In the case where *points* become tradable (***Airdrop Event*** case 3):

- The *mean conversion rate* is the volume weighted average price (VWAP) of one point (converted to the `Base Asset` is necessary) over `Minimum Trading Window` period prior to the ***Airdrop Event***.

The price of either tokens or points will be determined by the volume-weighted average price for the spot token/point on each `Valid Exchange` with at least `Minimum Traded Base Volume` in trading volume over the `Minimum Trading Window`.
If multiple `Valid Exchange`s list the spot price, the VWAP of each exchange will be averaged, weighting each for their total traded base currency volume.

