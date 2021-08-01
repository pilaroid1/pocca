#!/bin/bash
ip addr |grep "wlan0"|grep "UP"
ip addr |grep "wlan0"|grep "DOWN"
exit 0
