program record_function_cast.aleo;

interface data:
    owner as address;

function initialize:
    cast id.aleo into r0 as data;
    output r0 as data.private;