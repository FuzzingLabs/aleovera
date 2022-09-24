program groups.aleo;

function main:
    input r0 as group.private;
    double r0 into r1;
    neg r1 into r2;
    mul r0 2scalar into r3;
    add r3 r2 into r4;
    output r4 as group.private;