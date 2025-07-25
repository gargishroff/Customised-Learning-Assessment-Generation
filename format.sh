#!/bin/bash

set -x

black src
npx prettier . --write
