program record_and_token.aleo;

record token:
    owner as address.private;
    gates as u64.private;

function genesis:
    input r0 as address.private;
    input r1 as u64.private;
    cast r0 r1 into r2 as token.record;
    output r2 as token.record;