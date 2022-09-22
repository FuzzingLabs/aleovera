# ZK Coinflip

## QuickStart

### Build Guide

To compile this Aleo program, run:
```bash
aleo build
```

### Usage Guide
<details><summary>Commands and Playing the Game</summary>

In order to play coinflip, there must be two players. Navigate to the zk-coinflip aleo project. Then create two new aleo accounts:
```bash
aleo account new
>>>  Private Key  APrivateKey1zkp76mudqhsk6dYWnoxDsJeZHPgvykvCXZwv9PqvAo6fxVt
     View Key  AViewKey1iphJLAzN3KceJ45vCE2xRVbv6JcLaURNbpfBxMPRgHqC
      Address  aleo1kme6jxsfkt4gc8j5q3zv3x35u2lpm0vezmpnw3hx5qyg9lkt0yfqqf8gz0

aleo account new
>>>  Private Key  APrivateKey1zkp8fBkwb8NqGS8MMYtCJtZ7WLWZNTBArxqR93awsLXm47Y
     View Key  AViewKey1mNQd2StazxUQz52WqRX3G7Nbz24c8fEMkgKCLepHTSi4
      Address  aleo15gvfzykgaluzxkgeyk58vlngf9s24hnf5yurdest5kfgymut7y8s4xhtcx
```

Save the keys and addresses. Set the `program.json` private_key and address to one of the newly created aleo accounts. We'll refer to this address as Player 1, and the remaining address as Player 2.

```json
{
    "program": "coinflip.aleo",
    "version": "0.0.0",
    "description": "",
    "development": {
        "private_key": "APrivateKey1zkp76mudqhsk6dYWnoxDsJeZHPgvykvCXZwv9PqvAo6fxVt",
        "address": "aleo1kme6jxsfkt4gc8j5q3zv3x35u2lpm0vezmpnw3hx5qyg9lkt0yfqqf8gz0"
    },
    "license": "MIT"
}
```

Now, we need to issue a challenge as Player 1. This commits Player 1's choice and sends its hashed value to the opponent. Pick a random u64, and use Player 2's address as the opponent: `aleo run issue_challenge 8975u64 player_2_address`
```bash
aleo run issue_challenge 8975u64 aleo15gvfzykgaluzxkgeyk58vlngf9s24hnf5yurdest5kfgymut7y8s4xhtcx

>>> ➡️  Output

 • {
  owner: aleo15gvfzykgaluzxkgeyk58vlngf9s24hnf5yurdest5kfgymut7y8s4xhtcx.private,
  gates: 0u64.private,
  hashed_issuer_seed: 591924223095502087472303616041209416537242911135676306608411167537997318045field.private,
  issuer: aleo1kme6jxsfkt4gc8j5q3zv3x35u2lpm0vezmpnw3hx5qyg9lkt0yfqqf8gz0.private,
  _nonce: 5342744608757431758818220132535346504293655242366460928767706327432951369463group.public
}

✅ Executed 'coinflip.aleo/issue_challenge'
```

The output is an `issue` record owned by Player 2. Player 2 can choose to play this record and select their own input. Switch the `program.json` file to use Player 2's keys:

```json
{
    "program": "coinflip.aleo",
    "version": "0.0.0",
    "description": "",
    "development": {
        "private_key": "APrivateKey1zkp8fBkwb8NqGS8MMYtCJtZ7WLWZNTBArxqR93awsLXm47Y",
        "address": "aleo15gvfzykgaluzxkgeyk58vlngf9s24hnf5yurdest5kfgymut7y8s4xhtcx"
    },
    "license": "MIT"
}
```

Using the `issue` record and a new, random u64, Player 2 accepts the issued challenge: `aleo run accept_challenge random_u64 'issue.record'`
```bash
aleo run accept_challenge 2349587u64 '{
  owner: aleo15gvfzykgaluzxkgeyk58vlngf9s24hnf5yurdest5kfgymut7y8s4xhtcx.private,
  gates: 0u64.private,
  hashed_issuer_seed: 591924223095502087472303616041209416537242911135676306608411167537997318045field.private,
  issuer: aleo1kme6jxsfkt4gc8j5q3zv3x35u2lpm0vezmpnw3hx5qyg9lkt0yfqqf8gz0.private,
  _nonce: 5342744608757431758818220132535346504293655242366460928767706327432951369463group.public
}'

>>> ➡️  Output

 • {
  owner: aleo1kme6jxsfkt4gc8j5q3zv3x35u2lpm0vezmpnw3hx5qyg9lkt0yfqqf8gz0.private,
  gates: 0u64.private,
  hashed_issuer_seed: 591924223095502087472303616041209416537242911135676306608411167537997318045field.private,
  acceptor_seed: 2349587u64.private,
  acceptor: aleo15gvfzykgaluzxkgeyk58vlngf9s24hnf5yurdest5kfgymut7y8s4xhtcx.private,
  _nonce: 4550681717829692015148940403236459289479420029368110516858468927277669329595group.public
}

✅ Executed 'coinflip.aleo/accept_challenge'
```

This new `accept` record that was output is owned by Player 1, who can use it to complete the game.

Now, as Player 1, let's do that. Change the `program.json` file back to Player 1. We need to know if the combination of Player 1's and Player 2's numbers is even or odd. An odd number means Player 1 wins, and an even number means Player 2 wins.

With the `accept` record that contains the information about Player 2's u64, input the original u64 Player 1 chose, and two `complete` records will be output, with each player owning one. Run `aleo run complete_challenge original_u64 'accept.record'`:

```bash
aleo run complete_challenge 8975u64 '{
  owner: aleo1kme6jxsfkt4gc8j5q3zv3x35u2lpm0vezmpnw3hx5qyg9lkt0yfqqf8gz0.private,
  gates: 0u64.private,
  hashed_issuer_seed: 591924223095502087472303616041209416537242911135676306608411167537997318045field.private,
  acceptor_seed: 2349587u64.private,
  acceptor: aleo15gvfzykgaluzxkgeyk58vlngf9s24hnf5yurdest5kfgymut7y8s4xhtcx.private,
  _nonce: 4550681717829692015148940403236459289479420029368110516858468927277669329595group.public
}'

>>> ➡️  Outputs

 • {
  owner: aleo15gvfzykgaluzxkgeyk58vlngf9s24hnf5yurdest5kfgymut7y8s4xhtcx.private,
  gates: 0u64.private,
  issuer_number: 8975u64.private,
  acceptor_number: 2349587u64.private,
  issuer: aleo1kme6jxsfkt4gc8j5q3zv3x35u2lpm0vezmpnw3hx5qyg9lkt0yfqqf8gz0.private,
  acceptor: aleo15gvfzykgaluzxkgeyk58vlngf9s24hnf5yurdest5kfgymut7y8s4xhtcx.private,
  winner: aleo15gvfzykgaluzxkgeyk58vlngf9s24hnf5yurdest5kfgymut7y8s4xhtcx.private,
  _nonce: 7821022042970517276238305321354276039299884318471514585955941248832701552152group.public
}
 • {
  owner: aleo1kme6jxsfkt4gc8j5q3zv3x35u2lpm0vezmpnw3hx5qyg9lkt0yfqqf8gz0.private,
  gates: 0u64.private,
  issuer_number: 8975u64.private,
  acceptor_number: 2349587u64.private,
  issuer: aleo1kme6jxsfkt4gc8j5q3zv3x35u2lpm0vezmpnw3hx5qyg9lkt0yfqqf8gz0.private,
  acceptor: aleo15gvfzykgaluzxkgeyk58vlngf9s24hnf5yurdest5kfgymut7y8s4xhtcx.private,
  winner: aleo15gvfzykgaluzxkgeyk58vlngf9s24hnf5yurdest5kfgymut7y8s4xhtcx.private,
  _nonce: 6619870792418434601620346158941516947056656422429728274303408081789100726783group.public
}

✅ Executed 'coinflip.aleo/complete_challenge'
```

The `complete` records here detail both players' inputs, as well as who the winner is. the outputs here are similar to `offer_battleship`. The game is now complete.
</details>

## Strategy for Creating ZK Coinflip

Flipping a coin should be a game of chance -- a 50-50 for the player who takes heads and the player who takes tails. Such a simple game in the real world becomes much more complex on blockchains, as randomness isn't inherently supported. Randomness must either be provided by a [VRF](https://en.wikipedia.org/wiki/Verifiable_random_function) or by an oracle. In both cases, there is some degree of trust -- if the seed for the VRF is known to either player, then the VRF output is not random. Similarly, if the oracle is a bad actor, then the randomness they provide may not really be random. Instead, we can rely on the [Nash Equilibrium](https://en.wikipedia.org/wiki/Nash_equilibrium) to incentivize players to both provide a random value. We will add an input from each player, and then the winner will be chosen based on the resulting sum being odd or even. If only one player gives a random value, then the end result is still a 50-50. If both players use other strategies to select their inputs, they cannot hope to do better than a 50-50 unless they know the strategy of their opponent.

In Coinflip, Player 1 provides their u64 input, where the hash of that is stored in a record and sent to Player 2. Player 2 doesn't know what the original input was, so they can't force the summation to be odd or even. They provide another u64, which is sent back to Player 1 in another record. At this point, Player 1 must spend this record in order to collect a complete-record which details the winner of the coinflip. Player 1 must also input their initial u64, which is checked against the hash computed from it. If the hashes don't match, complete records aren't created and this transaction is aborted. If Player 1 is honest and puts in the original u64,then both Player 1 and Player 2 will receive complete-records. Now, Player 2 can see the unhashed original u64 input of Player 1 and double check for themself that the hash is correct.

## Extending Coinflip

The first question that might come up about this project is how to handle the case where Player 1 loses and doesn't want Player 2 to know this happened. After all, Player 1 could simply choose not to complete the game. This can be solved using blockheights as substitutes for timing. Once accessing blockheights is supported in aleo, we can set the block height when Player 2 responds to Player 1 with their own input. We can add a function to accept a record from Player 2 that checks the blockheight contained in the record against the current blockheight of the chain, and declare Player 2 the winner if Player 1 has not yet completed the game.

Another question might be about the security of hashing u64s. As this is intended to be a simple example, this is not the most secure creation of a coinflip. A bad Player 2 with a hash table of all u64s to fields could easily select their own input to force the end result to be even or odd. To that end, we could require Player 1 to input many u128 inputs, combined with generated salts in order to make each hash unique and expensive to create a hash-table for.
