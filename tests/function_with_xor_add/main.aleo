program function_with_xor_add.aleo;

function hello:
    input r0 as u16.public;
    input r1 as u16.private;
    input r2 as u32.private;
    input r3 as u32.private;
    xor r0 r1 into r4;
    add r3 r2 into r5;
    output r4 as u16.private;
    output r5 as u32.private;    