#!/bin/sh

python -m dfaccto_tpl -o ./gen -e simple.py -c ./example/cfg -t ./example/tpl \
          -m lib -c ./example/lib/cfg -t ./example/lib/tpl/
