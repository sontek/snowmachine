# How to release
## pypi
```bash
> python -m pip install build twine
> twine check dist/*
> twine upload dist/*
```

## docker
```bash
> VERSION=$(cat pyproject.toml|grep version|awk -F' ' '{ gsub(/"/, ""); print $3 }')
> docker build . -t sontek/snowmachine:$VERSION
> docker build . -t sontek/snowmachine:latest
> docker push sontek/snowmachine:$VERSION
> docker push sontek/snowmachine:latest
```

## nix
Update the version here:

https://github.com/NixOS/nixpkgs/blob/afcc0db199df11024b55813c0e8f713b23206db3/pkgs/by-name/sn/snowmachine/package.nix#L9

and send a pull request

