#!/bin/bash

# Install requirements
pip3 install -r requirements.txt

# for i in {1..13}
# do
#    python3 scrapping_validation.py --file "data/province$i.json"
#    sleep 5
# done

parallel -j 13 python3 scrapping_validation.py --file ::: data/province*.json