# Project-1-JWKS-server
This code consists of a server that returns JWT keys when given valid credentials. It has key expiration that expires in one hour however the code will still return an encrypted key but with the expiration time stamp. The repo also contains a TestSuite.py file that tests the authentication of the server. It tests valid credentials, valid credentials with expired key and invalid credentials.

I used ChatGPT to help me with some functions of the project. Specifically chatGPT helped me with the RSA key generation, serving the JWKS keys, how to post to the server through the Test Suite and how to output as a percent.
