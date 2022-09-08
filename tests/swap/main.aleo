// The 'swap.aleo' program.
program swap.aleo;
// The `swap` function transfers ownership of the record
// for token A to the record owner of token B, and vice-versa.
function swap:
    // Input the record for token A.
    input r0 as eth.aleo/eth.record;
    // Input the record for token B.
    input r1 as usdc.aleo/usdc.record;

    // Send the record for token A to the owner of token B.
    call eth.aleo/transfer r0 r1.owner r0.amount into r2 r3;

    // Send the record for token B to the owner of token A.
    call usdc.aleo/transfer r1 r0.owner r1.amount into r4 r5;

    // Output the new record for token A.
    output r2 as eth.aleo/eth.record;
    // Output the new record for token B.
    output r4 as usdc.aleo/usdc.record;