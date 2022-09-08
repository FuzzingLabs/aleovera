program record_function_selfcaller.aleo;

record data:
    owner as address.private;
    gates as u64.private;

function initialize:
    input r0 as data.record;
    cast self.caller r0.gates into r1 as data.record;
    output r1 as data.record;