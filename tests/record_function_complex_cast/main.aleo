program record_function_complex_cast.aleo;

record record_a:
    owner as address.private;
    gates as u64.private;

record record_b:
    owner as address.private;
    gates as u64.private;

function initialize:
    input r0 as record_a.record;
    input r1 as record_b.record;
    cast r0.owner r0.gates into r2 as record_a.record;
    cast r1.owner r1.gates into r3 as record_b.record;
    output r2 as record_a.record;
    output r3 as record_b.record;