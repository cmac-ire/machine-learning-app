#!/bin/sh

mkdir -p ~/.streamlit/

# Fixing the missing double quote and adding a shebang line
echo "\
[general]\n\
email = \"cfarr311y@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

# Setting a default value for PORT
PORT=${PORT:-8501}

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
