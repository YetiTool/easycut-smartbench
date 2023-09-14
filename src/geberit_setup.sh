git clone https://github.com/sameer/svg2gcode
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
. "$HOME/.cargo/env"
sudo ln -s /home/pi/.cargo/bin/cargo /usr/bin/cargo
cd svg2gcode
cargo add svg2gcode
cargo run --release -- examples/Vanderbilt_Commodores_logo.svg --off M3 --on M5 -o out.gcode
