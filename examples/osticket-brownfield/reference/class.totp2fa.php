<?php
/**
 * class.totp2fa.php  —  REFERENCE / ILLUSTRATIVE
 *
 * A TOTP (RFC 6238) two-factor backend for osTicket, plugged into the existing
 * TwoFactorAuthenticationBackend seam (include/class.2fa.php).
 *
 * THIS IS A TEACHING ARTIFACT, NOT A DROP-IN PATCH. It shows the shape of the
 * change and — more importantly — marks exactly which lines a senior human owns.
 * The osTicket-specific persistence/crypto/user hooks are left as clearly-labelled
 * integration points (// HUMAN-OWNED / // INTEGRATION). See NOTES.md.
 *
 * Ownership legend:
 *   [AGENT]  mechanical, safe for the agent to draft
 *   [HUMAN]  security-critical, senior must own and review line by line
 */
class TOTP2FABackend extends TwoFactorAuthenticationBackend {
    static $id   = "2fa-totp";
    static $name = /* @trans */ 'Authenticator app (TOTP)';
    static $desc = /* @trans */ 'Codes from an authenticator app (Google Authenticator, Authy, 1Password)';

    // RFC 6238 defaults that every authenticator app assumes.
    const DIGITS    = 6;
    const STEP      = 30;   // seconds
    const ALGO      = 'sha1';
    const DRIFT     = 1;    // [HUMAN] accept ±1 step only. Do NOT widen to "make it work".

    // ---- Enrollment UI -----------------------------------------------------[AGENT]
    // Show the Base32 secret and an otpauth:// URI; the template renders the QR.
    protected function getSetupOptions() {
        // INTEGRATION: a freshly generated secret is created at enrollment start and
        // held pending until confirmed (see validateSetup()). Never reuse an old one.
        return array(
            'secret' => new TextboxField(array(
                'id' => 1, 'label' => __('Secret key'),
                'configuration' => array('size' => 40, 'length' => 64),
                'hint' => __('Scan the QR code, or type this key into your authenticator app'),
            )),
        );
    }

    // The 6-digit code the user reads from their app.
    protected function getInputOptions() {
        return array(
            'token' => new TextboxField(array(
                'id' => 1, 'label' => __('Verification Code'), 'required' => true,
                'validator' => 'number',
                'configuration' => array(
                    'size' => 40, 'length' => 6,
                    'autocomplete' => 'one-time-code',
                    'inputmode' => 'numeric', 'pattern' => '[0-9]*',
                    'validator-error' => __('Invalid Code format'),
                ),
            )),
        );
    }

    // ---- send(): meaningless for TOTP -------------------------------------[AGENT]
    // The base abstraction expects a code to be "sent". TOTP sends nothing — the app
    // generates it. Inert no-op. It must not leak the secret or do anything observable.
    function send($user) {
        return true;
    }

    // ---- Secret generation -------------------------------------------------[HUMAN]
    // CSPRNG, >=160 bits, Base32 via osTicket's existing Base32 class.
    static function generateSecret() {
        $bytes = random_bytes(20);              // [HUMAN] random_bytes, never rand()/mt_rand()
        return Base32::encode($bytes);          // INTEGRATION: include/class.base32.php
    }

    // otpauth:// provisioning URI for the QR code. Issuer/label only — no PII beyond username.
    static function provisioningUri($secretBase32, $accountName, $issuer = 'osTicket') {
        return sprintf('otpauth://totp/%s:%s?secret=%s&issuer=%s&algorithm=SHA1&digits=%d&period=%d',
            rawurlencode($issuer), rawurlencode($accountName),
            $secretBase32, rawurlencode($issuer), self::DIGITS, self::STEP);
    }

    // ---- HOTP / TOTP core (RFC 4226 / 6238) -------------------------------[AGENT]
    // Pure function. This is the part the RFC 6238 test vectors verify exactly, so it
    // cannot be faked by a mock-the-implementation test (slop signature #1).
    static function hotp($keyBinary, $counter, $digits = self::DIGITS) {
        $msg  = pack('N2', ($counter >> 32) & 0xffffffff, $counter & 0xffffffff); // 8-byte big-endian
        $hash = hash_hmac(self::ALGO, $msg, $keyBinary, true);
        $off  = ord($hash[strlen($hash) - 1]) & 0x0f;                              // dynamic truncation
        $bin  = ((ord($hash[$off])   & 0x7f) << 24)
              | ((ord($hash[$off+1]) & 0xff) << 16)
              | ((ord($hash[$off+2]) & 0xff) << 8)
              |  (ord($hash[$off+3]) & 0xff);
        return str_pad((string)($bin % (10 ** $digits)), $digits, '0', STR_PAD_LEFT);
    }

    static function totpAt($secretBase32, $time = null, $offsetSteps = 0) {
        $time = $time ?? time();
        $step = intdiv($time, self::STEP) + $offsetSteps;
        return self::hotp(Base32::decode($secretBase32), $step);
    }

    // ---- Verification ------------------------------------------------------[HUMAN]
    // Constant-time compare + replay protection + bounded drift. Every line here is
    // owned by a senior reviewer. Do NOT copy the email path's strcmp().
    function validate($form, $user) {
        if (!($form->isValid() && ($clean = $form->getClean()) && $clean['token']))
            return false;
        $submitted = (string) $clean['token'];

        // INTEGRATION: load + decrypt the user's confirmed secret and the last-consumed
        // step. $cfg = $user->get2FAConfig($this->getId()); $secret = Crypto::decrypt($cfg['secret']);
        $secret    = /* INTEGRATION */ self::loadSecretFor($user);
        $lastStep  = /* INTEGRATION */ self::loadLastStepFor($user);  // int or null
        if (!$secret)
            return false;

        // Strike/timeout machinery from the base class still applies. [HUMAN]
        $store = &$_SESSION['_2fa'][$this->getId()];
        $store['strikes'] = ($store['strikes'] ?? 0) + 1;
        if ($store['strikes'] > $this->getMaxStrikes())
            throw new ExpiredOTP(__('Too many attempts'));

        $now  = intdiv(time(), self::STEP);
        $matchedStep = null;
        // Evaluate the full drift window before deciding, so timing doesn't leak which
        // step matched. hash_equals() is the constant-time primitive — never == / strcmp.
        for ($d = -self::DRIFT; $d <= self::DRIFT; $d++) {
            $candidate = self::hotp(Base32::decode($secret), $now + $d);
            if (hash_equals($candidate, $submitted))
                $matchedStep = $now + $d;
        }
        if ($matchedStep === null)
            return false;

        // Replay protection: a given step may be consumed once. [HUMAN]
        if ($lastStep !== null && $matchedStep <= $lastStep)
            return false;

        // INTEGRATION: persist $matchedStep as the new last-consumed step (atomic).
        self::storeLastStepFor($user, $matchedStep);

        $this->onValidate($user);   // base-class housekeeping (clear 2FA flags)
        return true;
    }

    // ---- Integration stubs (osTicket-specific; wired by the human) ----------------
    // These exist so the file is readable end-to-end. In the real change they map to
    // $user->get2FAConfig(), Crypto::encrypt/decrypt, and an upgrade-stream migration
    // that adds the per-user secret + last_step columns. They are NOT implemented here
    // on purpose — persistence and crypto are human-owned decisions.
    static protected function loadSecretFor($user)        { /* INTEGRATION */ return null; }
    static protected function loadLastStepFor($user)      { /* INTEGRATION */ return null; }
    static protected function storeLastStepFor($user,$s)  { /* INTEGRATION */ }
}

// Registration — backends self-register so the seam discovers them. [AGENT]
// TwoFactorAuthenticationBackend::register('TOTP2FABackend');
