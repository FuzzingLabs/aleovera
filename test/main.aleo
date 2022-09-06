// The 'test.aleo' program.
program test.aleo;

record token:
    owner as address.private;
    gates as u64.private;
    amount as u64.private;

interface array3:
    a0 as u32;
    a1 as u32;
    a2 as u32;

function sum_one_to_array3:
    input r0 as array3.private;
    add r0.a0 1u32 into r1;
    add r0.a1 1u32 into r2;
    add r0.a2 1u32 into r3;
    cast r1 r2 r3 into r4 as array3;
    output r4 as array3.private;


function hello:
    input r0 as u16.public;
    input r1 as u16.private;
    input r2 as u32.private;
    input r3 as u32.private;
    xor r0 r1 into r4;
    add r3 r2 into r5;
    output r4 as u16.private;
    output r5 as u32.private;
