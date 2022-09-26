program test_print_attribute_type.aleo;

interface Row:
    c1 as u8;
    c2 as u8;
    c3 as u8;

interface Board:
    r1 as Row;
    r2 as Row;
    r3 as Row;

closure hell:
    input r0 as Board;
    input r1 as u8;
    is.eq r0.r1.c1 r1 into r2;
    is.eq r0.r1.c2 r1 into r3;
    and r2 r3 into r4;
    output r4 as boolean;

function hello:
    input r0 as Board.public;
    input r1 as u8.public;
    is.eq r0.r1.c1 r1 into r2;
    is.eq r0.r1.c2 r1 into r3;
    and r2 r3 into r4;
    output r4 as boolean.public;