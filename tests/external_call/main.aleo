import difference.aleo;
import product.aleo;
import quotient.aleo;
import sum.aleo;
program external_call.aleo;

function main:
    input r0 as u32.public;
    input r1 as u32.private;
    call product.aleo/product r0 r1 into r2;
    call quotient.aleo/quotient r2 r1 into r3;
    call sum.aleo/sum r3 r0 into r4;
    call difference.aleo/difference r4 r3 into r5;
    assert.eq r5 r0;
    output r5 as u32.private;
