program finalize_compute.aleo;

mapping account:
    key owner as address.public;
    value amount as u64.public;

function compute:
    input r0 as address.public;
    input r1 as u64.public;
    input r2 as u64.public;
    add r1 r2 into r3;
    finalize r0 r3;

finalize compute:
    input r0 as address.public;
    input r1 as u64.public;
    increment account[r0] by r1;