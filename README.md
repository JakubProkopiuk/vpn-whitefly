# Custom VPN Service – Recruitment Task

## Features

- Secure VPN tunnel using Linux TUN devices (IP-level tunneling)
- Key generation (RSA for authentication, AES for encrypted session)
- Simple user authentication (login & password)
- Secure session key exchange (RSA → AES)
- Encrypted bidirectional tunnel (AES-256-CBC)
- All traffic (ICMP, TCP, UDP, etc.) is tunneled
- Can be extended with SOCKS5 if required

---

## How To Use

1. **Key Generation**
    ```
    python3 generate_keys.py
    ```

2. **Key Exchange**
    - Start `key_exchange_server.py` on the server.
    - Start `key_exchange_client.py` on the client.

3. **Start the Encrypted Tunnel**
    - On the server:
        ```
        sudo python3 tunnel_server.py
        ```
    - On the client:
        ```
        sudo python3 tunnel_client.py
        ```

4. **Routing**
    - On the client, add route for the VPN:
        ```
        sudo ip route add 10.0.0.1/32 dev tun1
        ```

5. **Testing**
    - From client:
        ```
        ping -I tun1 10.0.0.1
        ```
    - (Optional) On server, monitor packets:
        ```
        sudo tcpdump -i tun0 -n icmp
        ```

---

## Weaknesses & Security Recommendations

- **No perfect forward secrecy**  
  *Mitigation*: Use ephemeral Diffie-Hellman exchange for session keys.
- **No replay protection**  
  *Mitigation*: Add timestamp/counter to packets, reject duplicates.
- **No integrity check for whole packets**  
  *Mitigation*: Add HMAC (hash-based message authentication code) to each packet.
- **Brute-force possible on login/password**  
  *Mitigation*: Limit login attempts, add delay/lockout, or add 2FA.
- **No mutual authentication**  
  *Mitigation*: Let client verify server as well.
- **Session key never rotates**  
  *Mitigation*: Rotate the session key periodically or after certain data amount.
- **Keys stored unencrypted**  
  *Mitigation*: Store private keys encrypted on disk (use passphrase).

---

## Author

Jakub Prokopiuk

---
