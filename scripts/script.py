#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the miniMaxSum function below.
def miniMaxSum(arr):
  array_sum = sum(arr)
  
  new_array = []
  for i in arr:
    new_array.append(array_sum - i)

  return [max(new_array), min(new_array)]
  
  
  
if __name__ == '__main__':

    arr = list(map(int, input().rstrip().split()))
    miniMaxSum(arr)
