# Infinite-QR

The challenge here is simple, find the flag. I hope your scroll wheel works...

Flag format: `flag{...}`

### How To Run

```
$ docker build -t infiniteqr .
$ docker run -p 5000:5000 infiniteqr
```

### Flag

```
flag{h0w_l0ng_d1d_y0u_scr0ll_t0_f1nd_th1s?}
```

### Walkthrough

- This is a scripting challenge to read the QR codes and decode them, searching for `flag{`:

