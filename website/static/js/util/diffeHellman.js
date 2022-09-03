function genPrime() {
    const rand = Math.floor(Math.random() * (2 ** 1024)) + 1340780792994259709957402499820584612747936582059239337772356
    1443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084096;
    largest_prime = 2
    let i = 1000
    let largest_prime;
    while (i < rand) {
        let isprime = "True"
        let test;
        for (test === 0; test < i; test++) {
            if (i % test !== 0) {
                let isprime = "False"
            }
        }
        if (isprime === "True") {
            largest_prime = i
        }
        i++
    }
    return largest_prime
}

const multiplier = 15804226527751178695380278391698825132884832505826661964650543292987095063276128381793154007412858843
413860969728256459754000845886356821133417000665601057484568726303869347498937196495076974306335798802188133994901496053
8939636010924483425268942107851645455922872203315568744818583038121046742253841446088891

function publicKey(privateKey) {
    return privateKey * multiplier
}

function generateSharedKey(privateKey, otherPublicKey) {
    return privateKey * otherPublicKey
}

function getOtherKey() {
    return -1
}
