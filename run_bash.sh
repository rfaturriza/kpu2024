#!/bin/bash

# Install requirements
pip3 install -r requirements.txt

parallel -j 3 python3 scrapping_validation.py --file ::: data/province*.json