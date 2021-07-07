/* { system ? "x86_64-darwin", pkgs ? import <nixpkgs> { inherit system; }
}:
pkgs.dockerTools.buildLayeredImage { # helper to build Docker image
  name = "nix-hello";                # give docker image a name
  tag = "latest";                    # provide a tag
  contents = [ pkgs.hello ];         # packages in docker image
} */
{ pkgs ? import <nixpkgs> { system = "x86_64-linux"; } }:

pkgs.dockerTools.buildImage {
  name = "hello-docker";
  config = {
    Cmd = [ "${pkgs.hello}/bin/hello" ];
  };
}
