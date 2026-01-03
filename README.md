# Jioreboot

Jioreboot reverse-engineers Jio Fiber's dashboard (or Centram Home Gateway) API
and reboots the router on command. This is useful for scheduling restarts or
just casual ones if you despise like leaving your room like me :D

It's done by sending a POST request to the router's login page and then using the cookie from the response headers to make a POST request to the reboot page. See the source code for more underlying details.

# Demo
![](https://files.catbox.moe/gcrora.png)

# Usage
Usage is simple. Install the project via:

```bash
pip install git+https://github.com/eeriemyxi/jioreboot
```

Then simply run `jioreboot` in a shell:

```
❯ jioreboot
ERROR: Config file /home/myxi/.config/jioreboot/config.json not found
```

It will error out with a config location. Simply create that file and fill in
these details under there:

```json
{
	"username": "admin",
	"password": "mypassword1234"
}
```

That's all. Try running `jioreboot` again at your convenience.
