import difference.aleo;
import product.aleo;
import quotient.aleo;
import sum.aleo;
program multiple_calls.aleo;

record data:
    owner as address.private;
    gates as u64.private;

function initialize:
    input r0 as u32.public;
    input r1 as u32.private;
    call product.aleo/product r0 r1 into r2;
    call quotient.aleo/quotient r2 r1 into r3;
    call sum.aleo/sum r3 r0 into r4;
    call difference.aleo/difference r4 r3 into r5;
    assert.eq r5 r0;
    output r5 as u32.private;


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


function main:
    input r0 as u32.public;
    input r1 as u32.private;
    call product.aleo/product r0 r1 into r2;
    call quotient.aleo/quotient r2 r1 into r3;
    call sum.aleo/sum r3 r0 into r4;
    call difference.aleo/difference r4 r3 into r5;
    assert.eq r5 r0;
    output r5 as u32.private;
