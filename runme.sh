#!/data/data/com.termux/files/usr/bin/bash
cd ~/nacho/termux-backend
dos2unix **/*
tmux new-session -d -s run_myapi 'uvicorn main:app --reload'
