import issue.aleo;
import accept.aleo;
import complete.aleo;

// The 'coinflip.aleo' program.
program coinflip.aleo;

function issue_challenge:
    input r0 as u64.private; // issuer's seed, should be a random u64
    input r1 as address.private; // the acceptor's address

    hash.psd8 r0 into r2; // turn the issuer seed into a field

    call issue.aleo/issue_challenge r2 r1 into r3;

    output r3 as issue.aleo/issue.record;

function accept_challenge:
    input r0 as u64.private; // the acceptor's seed, should be a random u64
    input r1 as issue.aleo/issue.record; // the issue record that was issued to the acceptor

    call accept.aleo/accept_challenge r1.issuer r1.hashed_issuer_seed r0 into r2;

    output r2 as accept.aleo/accept.record;

function complete_challenge:
    input r0 as u64.private; // original issuer's seed
    input r1 as accept.aleo/accept.record;

    hash.psd8 r0 into r2; // turn the issuer seed into a hashed field

    assert.eq r2 r1.hashed_issuer_seed; // make sure the issuer doesn't change numbers here

    add.w r0 r1.acceptor_seed into r3;
    mod r3 2u64 into r4;
    is.eq r4 1u64 into r5;
    ternary r5 self.caller r1.acceptor into r6; // winner

    call complete.aleo/complete_challenge r1.acceptor r1.acceptor_seed r0 r6 into r7 r8;

    output r7 as complete.aleo/complete.record;
    output r8 as complete.aleo/complete.record;