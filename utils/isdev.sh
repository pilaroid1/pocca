#!/bin/bash
grep -q overlay /boot/cmdline.txt
echo $?

