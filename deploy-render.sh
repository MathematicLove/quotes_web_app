#!/bin/bash

if [ ! -f "README.md" ]; then
    echo "Load from root!"
    exit 1
fi

if [ ! -d ".git" ]; then
    echo "Not git"
    echo "run this: git init && git add . && git commit -m 'Initial commit'"
    exit 1
fi

if [ -n "$(git status --porcelain)" ]; then
    echo "run: git add . && git commit -m 'Update for deployment'"
    read -p "Next: (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
