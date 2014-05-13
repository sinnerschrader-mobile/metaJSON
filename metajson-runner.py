#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Convenience wrapper for running metajson directly from source tree."""



import sys

if __name__ == '__main__':
    from metajson.readJSON import main
    sys.exit(main(sys.argv))
