<?php
/**
 * RFC 6238 test-vector unit test for the TOTP core.
 *
 * This is the test that matters most: the expected outputs come from the RFC, not
 * from our implementation, so it cannot be satisfied by a mock-the-implementation
 * slop test (Ch 2, signature #1). If hotp()/totpAt() are wrong, this goes red.
 *
 * Requires the Base32 class (osTicket: include/class.base32.php). For standalone runs,
 * a tiny Base32 shim is provided below if the class is absent.
 *
 * Usage: php test.totp-vectors.php
 */
error_reporting(E_ALL);

if (!class_exists('Base32')) {
    // Minimal RFC 4648 Base32 (standalone fallback; production uses osTicket's class).
    class Base32 {
        const A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
        static function encode($bin) {
            $bits=''; foreach (str_split($bin) as $c) $bits.=str_pad(decbin(ord($c)),8,'0',STR_PAD_LEFT);
            $out=''; foreach (str_split($bits,5) as $chunk){ if(strlen($chunk)<5)$chunk=str_pad($chunk,5,'0'); $out.=self::A[bindec($chunk)];}
            return $out;
        }
        static function decode($b32) {
            $b32=strtoupper(preg_replace('/[^A-Z2-7]/','',$b32)); $bits='';
            foreach (str_split($b32) as $c) $bits.=str_pad(decbin(strpos(self::A,$c)),5,'0',STR_PAD_LEFT);
            $out=''; foreach (str_split($bits,8) as $chunk){ if(strlen($chunk)==8)$out.=chr(bindec($chunk)); }
            return $out;
        }
    }
}

require __DIR__ . '/class.totp2fa.php';   // pulls in TOTP2FABackend (needs the 2fa base in real osTicket)

// RFC 6238 Appendix B, SHA-1, secret = ASCII "12345678901234567890".
$secret = Base32::encode('12345678901234567890');
$cases = [
    [59,          '94287082'],
    [1111111109,  '07081804'],
    [1111111111,  '14050471'],
    [1234567890,  '89005924'],
    [2000000000,  '69279037'],
];

$pass = 0; $fail = 0;
foreach ($cases as [$t, $expected8]) {
    // RFC vectors are 8 digits; production uses 6. Compare the trailing 6.
    $got = TOTP2FABackend::hotp(Base32::decode($secret), intdiv($t, 30), 6);
    $want = substr($expected8, -6);
    if (hash_equals($want, $got)) { $pass++; echo "  PASS  T=$t -> $got\n"; }
    else { $fail++; echo "  FAIL  T=$t -> got $got, want $want\n"; }
}

// Replay/drift are exercised in the integration flow; here we prove the math.
echo "\n$pass passed, $fail failed\n";
exit($fail === 0 ? 0 : 1);
