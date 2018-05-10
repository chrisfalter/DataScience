REM (5) X-long nets
python nntrain.py tanh "256,128,64,32,16" > c:/temp/tanh_256-128-64-32-16.csv
python nntrain.py relu "256,128,64,32,16" > c:/temp/relu_256-128-64-32-16.csv
python nntrain.py tanh "192,64,32,16,8" > c:/temp/tanh_192-64-32-16-8.csv
python nntrain.py relu "192,64,32,16,8" > c:/temp/relu_192-64-32-16-8.csv
python nntrain.py tanh "192,192,32,32,8" > c:/temp/tanh_192-192-32-32-8.csv
python nntrain.py relu "192,192,32,32,8 > c:/temp/relu_192-192-32-32-8.csv
python nntrain.py tanh "128,64,32,16,8" > c:/temp/tanh_128-64-32-16-8.csv
python nntrain.py relu "128,64,32,16,8" > c:/temp/relu_128-64-32-16-8.csv
python nntrain.py tanh "64,32,24,16,8" > c:/temp/tanh_64-32-24-16-8.csv
python nntrain.py relu "64,32,24,16,8" > c:/temp/relu_64-32-24-16-8.csv
REM (4) long nets
python nntrain.py tanh "256,96,48,16" > c:/temp/tanh_256-96-48-16.csv
python nntrain.py relu "256,96,48,16" > c:/temp/relu_256-96-48-16.csv
python nntrain.py tanh "192,64,32,8" > c:/temp/tanh_192-64-32-8.csv
python nntrain.py relu "192,64,32,8" > c:/temp/relu_192-64-32-8.csv
python nntrain.py tanh "128,64,16,8" > c:/temp/tanh_128-64-16-8.csv
python nntrain.py relu "128,64,16,8" > c:/temp/relu_128-64-16-8.csv
REM (3) medium nets
python nntrain.py tanh "256,96,32" > c:/temp/tanh_256-96-32.csv
python nntrain.py relu "256,96,32" > c:/temp/relu_256-96-32.csv
python nntrain.py tanh "192,64,16" > c:/temp/tanh_192-64-16.csv
python nntrain.py relu "192,64,16" > c:/temp/relu_192-64-16.csv
python nntrain.py tanh "128,64,16" > c:/temp/tanh_128-64-16.csv
python nntrain.py relu "128,64,16" > c:/temp/relu_128-64-16.csv
python nntrain.py tanh "96,64,32" > c:/temp/tanh_96-64-32.csv
python nntrain.py relu "96,64,32" > c:/temp/relu_96-64-32.csv
python nntrain.py tanh "192,192,48" > c:/temp/tanh_192-192-48.csv
python nntrain.py relu "192,192,48" > c:/temp/relu_192-192-48.csv
REM (2) short nets
python nntrain.py tanh "256,128" > c:/temp/tanh_256-128.csv
python nntrain.py relu "256,128" > c:/temp/relu_256-128.csv
python nntrain.py tanh "192,192" > c:/temp/tanh_192-192.csv
python nntrain.py relu "192,192" > c:/temp/relu_192-192.csv
python nntrain.py tanh "192,64" > c:/temp/tanh_192-64.csv
python nntrain.py relu "192,64" > c:/temp/relu_192-64.csv
python nntrain.py tanh "64,64" > c:/temp/tanh_64-64.csv
python nntrain.py relu "64,64" > c:/temp/relu_64-64.csv
python nntrain.py tanh "64,16" > c:/temp/tanh_64-16.csv
python nntrain.py relu "64,16" > c:/temp/relu_64-16.csv

