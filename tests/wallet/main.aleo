import token.aleo;
program wallet.aleo;

function transfer:
    input r0 as token.aleo/token.record;
    input r1 as address.private;
    input r2 as u64.private;
    call token.aleo/transfer r0 r1 r2 into r3 r4;
    output r3 as token.aleo/token.record;
    output r4 as token.aleo/token.record;