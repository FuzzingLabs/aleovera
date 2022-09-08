// The 'token3.aleo' program.
program token3.aleo;

mapping account:
    // The token owner.
    key owner as address.public;
    // The token amount.
    value amount as u64.public;

// The function `mint_public` issues the specified token amount
// for the token receiver publicly on the network.
function mint_public:
    // Input the token receiver.
    input r0 as address.public;
    // Input the token amount.
    input r1 as u64.public;
    // Mint the tokens publicly.
    finalize r0 r1;

// The finalize scope of `mint_public` increments the
// `account` of the token receiver by the specified amount.
finalize mint_public:
    // Input the token receiver.
    input r0 as address.public;
    // Input the token amount.
    input r1 as u64.public;

    // Increments `account[r0]` by `r1`.
    // If `account[r0]` does not exist, it will be created.
    // If `account[r0] + r1` overflows, `mint_public` is reverted.
    increment account[r0] by r1;