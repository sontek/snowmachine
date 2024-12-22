snowmachine
=======

A python script that allows your terminal to snow. View it in action here:

* https://asciinema.org/a/624427
* https://asciinema.org/a/376826
* https://asciinema.org/a/376827

*homebrew*:

```bash
brew tap sontek/snowmachine
brew install sontek/snowmachine/snowmachine
```

*pypi*:
```bash
pip install snowmachine
```

*nix*:
```bash
nix-shell -p snowmachine --command snowmachine
```

*docker*:
```bash
docker run --rm -ti sontek/snowmachine
```

Getting Started
---------------
You can make it snow:

```bash
$ snowmachine snow
```
<img src="https://cdn.zappy.app/b3cb0d489960b5c545ee95aad08c6da1.png" />

or render a tree:

```bash
$ snowmachine tree
```
<img src="https://cdn.zappy.app/3c3a71af31d5a2a6cf0bb77de8b94d13.png" />

You can also tell it to stack the snow if you prefer.

```bash
$ snowmachine snow --stack=pile
```

If you don't like the unicode particles you can tell it to use
asterisk or some other character.  If you use cmd.exe for example,
this will be required.

```bash
$ snowmachine snow --stack=pile --particle="*"
```

You can also change the particle colors if you would like:

```bash
$ snowmachine snow --color=rainbow
```

In addition you can change the speed of particles:
```bash
$ snowmachine --speed=5
```


You can find a bash(shell) script version of this here:
https://gist.github.com/sontek/1505483


Screenshot:

![Screenshot 1](https://i.imgur.com/r8MRa17.png)
![Screenshot 2](https://i.imgur.com/d8rH4de.png)

## Star Options

The Christmas tree can now be decorated with different star styles on top. Use the `--star` option with the `tree` command to add a star. Available styles are:

- `classic`: A traditional 5-point star pattern made with asterisks
- `diamond`: A diamond-shaped star pattern
- `patrick`: A playful star pattern resembling a starfish

Example usage:

```bash
$ snowmachine tree --star=classic
```
