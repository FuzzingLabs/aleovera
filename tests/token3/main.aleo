program token3.aleo;

mapping account:
    key owner as address.public; 
    value amount as u64.public;

function mint_public: 
    input r0 as address.public;  
    input r1 as u64.public;
    finalize r0 r1;

finalize mint_public:
    input r0 as address.public;
    input r1 as u64.public;
    increment account[r0] by r1;