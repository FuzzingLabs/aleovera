program core.aleo;

function main:
    input r0 as field.private;
    hash.bhp256 r0 into r1;
    hash.psd2 r1 into r2;
    commit.bhp256 r2 15scalar into r3;
    output r3 as field.private;