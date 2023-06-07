#!/bin/bash

input_dir="downloaded_segments"
output_dir="decrypted_segments"
key=$(hexdump -v -e '/1 "%02X"' < 2160.key)

mkdir -p "$output_dir"

for input_file in "$input_dir"/*.ts; do
    output_file="$output_dir/$(basename "$input_file")"
    openssl enc -d -aes-128-cbc -in "$input_file" -out "$output_file" -K "$key" -iv 0
done