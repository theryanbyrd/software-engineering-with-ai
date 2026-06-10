<?php
/**
 * Characterization test — existing osTicket 2FA contract (Tier 1, structural).
 *
 * Pins the behavior/contract we are about to stand next to before adding a TOTP backend.
 * Same idiom as osTicket's own setup/test checks: assertions over source, no DB required.
 *
 * Usage: php test.2fa-email.php /path/to/osticket-src
 * Exit 0 if all invariants hold, 1 otherwise.
 */
error_reporting(E_ALL & ~E_DEPRECATED);

$src = $argv[1] ?? './osticket-src';
$file = rtrim($src, '/') . '/include/class.2fa.php';

$pass = 0; $fail = 0;
function check($name, $cond) {
    global $pass, $fail;
    if ($cond) { $pass++; echo "  PASS  $name\n"; }
    else       { $fail++; echo "  FAIL  $name\n"; }
}

echo "Characterization: osTicket 2FA contract\n";
echo "Source: $file\n\n";

if (!is_file($file)) {
    fwrite(STDERR, "FATAL: cannot find include/class.2fa.php under '$src'\n");
    exit(2);
}
$code = file_get_contents($file);

// --- the abstraction we extend -------------------------------------------------
check('abstract TwoFactorAuthenticationBackend exists',
    (bool) preg_match('/abstract\s+class\s+TwoFactorAuthenticationBackend\b/', $code));
check('registration entry point register() exists',
    strpos($code, 'function register(') !== false);
check('lookup path getBackend()/allRegistered() exists',
    strpos($code, 'function getBackend(') !== false && strpos($code, 'function allRegistered(') !== false);

// --- required method surface (a new backend must satisfy this) ------------------
foreach (['send', 'validate', 'getSetupForm', 'getInputForm'] as $m) {
    check("interface method '$m' present", strpos($code, "function $m(") !== false);
}

// --- the one existing backend ---------------------------------------------------
check('Email2FABackend exists', strpos($code, 'class Email2FABackend') !== false);
check("Email backend id is '2fa-email'",
    (bool) preg_match('/\$id\s*=\s*"2fa-email"/', $code));
check('Email OTP is a 6-digit number (Misc::randNumber(6))',
    strpos($code, 'Misc::randNumber(6)') !== false);

// --- strike / timeout machinery we must preserve --------------------------------
check('strike limiting via getMaxStrikes() in _validate()',
    strpos($code, 'getMaxStrikes()') !== false);
check('timeout/expiry via getTimeout() + ExpiredOTP',
    strpos($code, 'getTimeout()') !== false && strpos($code, 'ExpiredOTP') !== false);

// --- KNOWN BASELINE: non-constant-time comparison (recorded on purpose) ---------
// We are NOT asserting this is correct. We pin it so the TOTP review must make a
// conscious decision about comparison timing instead of inheriting it by accident.
$nonct = (bool) preg_match('/strcmp\(\s*\$store\[\'otp\'\]/', $code);
check('BASELINE pinned: base _validate() uses strcmp() (non-constant-time)', $nonct);
if ($nonct) {
    echo "        ^ tracked baseline. A TOTP secret comparison MUST be constant-time;\n";
    echo "          do not copy the email path's strcmp() for secret-derived codes.\n";
}

echo "\n$pass passed, $fail failed\n";
exit($fail === 0 ? 0 : 1);
