// The 'compute_add.aleo' program.
program compute_add.aleo;

function compute:
    add 1u32 2u32 into r0;
    output r0 as u32.private;