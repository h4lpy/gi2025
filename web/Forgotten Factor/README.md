# Forgotten Factor

My friend has got really into web development but knows nothing about security. He claims to have implemented proper MFA but I'm not so sure, can you get the flag from this login form?

Flag format: `flag{...}`

### How To Run



### Flag

```
flag{s3ri0usly_b4d_mf4_impl3ment4t1on}
```

### Walkthrough

- Login form accepts any username:password combination
- Subsequent MFA form requires a 64-digit string
- Submitting a valid string 3 times reveals the token