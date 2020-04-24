# Beyond proof of stake

GitHub issue: [#12](https://github.com/vegaprotocol/research/issues/12)

## Description

Both proof of work and proof of stake create a validator economics that is not necessarily
in the best interest of blockchain resilience. In proof of work settings, validators tend
to cluster to geographic areas with favourable conditions (primarily cheap energy). In the
Bitcoin case, this has led to a concentration of far more than 50% of validator capacity in
China, which endangers the point of decentralisation. In proof of stake networks, validators might cluster around available capital and concentrated with service providers. Furthermore, with the increasing tendency towards cloud computing, there is a real danger that seemingly independent validators all effectively run on a set of three or four cloud providers.

Techniques exist to design more complex voting schemes - e.g., requiring 2/3 of the votes
of 2/3 of a given set of geographic domains. This does raise the question on what policy these techniques should be used to implement.

**Research problem:** Analyse factors in validator distribution that are likely to compromise
the positive effects of decentralisation, and the are likely to occur due to economic or other factors. Assuming that technical implementation is not a problem, propose a voting policy that would minimise the identified effects.

**Note:** There are some constraints on what policy can be implemented in a Byzantine setting (a generalised version of the 1/3 constraint) that would be useful to take into account.
