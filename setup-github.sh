#!/bin/bash
if [ ! -d ".git" ]; then
    echo "Not git"
    exit 1
fi

read -p "Created on GitHub? (y/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "URL of repo ?"
    read -p "URL: " github_url
    
    if [ -n "$github_url" ]; then
        git remote add origin "$github_url"
        git branch -M main
        git push -u origin main
        echo "RUN! : ./deploy-render.sh"
    else
        echo "WRONG URL"
    fi
else
    echo "First create in GitHub"
fi
