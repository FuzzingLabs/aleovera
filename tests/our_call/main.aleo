// The 'our_call.aleo' program.
program our_call.aleo;

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
    call execute r0 r1 into r2 r3 r4;
    output r2 as field.private;
    output r3 as field.private;
    output r4 as field.private;
