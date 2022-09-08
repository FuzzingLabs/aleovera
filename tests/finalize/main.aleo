
program finalize.aleo;

record token:
    owner as address.private;
    gates as u64.private;
    amount as u64.private;

mapping account:
    key owner as address.public;
    value amount as u64.public;

function transfer_public_to_private:
    input r0 as u64.public;
    input r1 as u64.public;
    add r0 r1 into r2;
    output r2 as u64.public;
    finalize self.caller r1;

finalize transfer_public_to_private:
    input r0 as address.public;
    input r1 as u64.public;
    decrement account[r0] by r1;
    add r1 r1 into r2;
    increment account[r0] by r1;
    output r2 as u64.public;