// The 'token1.aleo' program.
program token1.aleo;

record token:
    owner as address.private;
    gates as u64.private;
    token_amount as u64.private;

// (a + (a + b)) + (a + b) == (3a + 2b)
closure execute:
    input r0 as field;
    input r1 as field;
    add r0 r1 into r2;
    add r0 r2 into r3;
    add r2 r3 into r4;
    output r4 as field;
    output r3 as field;
    output r2 as field;

function compute:
    input r0 as field.private;
    input r1 as field.public;
    input r2 as token.record;
    cast r2.owner r2.gates r2.token_amount into r3 as token.record;
    call execute r0 r1 into r4 r5 r6;
    output r3 as token.record;
    output r4 as field.private;
    output r5 as field.private;
    output r6 as field.private;