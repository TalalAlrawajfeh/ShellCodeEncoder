# ShellCodeEncoder

In my spare time, I had fun with reverse engineering, writing exploits, fuzzing, pentesting and all that good stuff. So once I stumbled across a scenario that I needed to deliver shellcode only in printable ASCII characters. I know that there are lots of encoders out there and much better than mine. But I wanted to learn everything from scratch, so I decided that I will write a shellcode encoder that encodes a binary containing the shellcode into printable ASCII characters and sticks a decoder before it. The decoder must also be entirely in printable ASCII characters. So what I did was that I grabbed the intel instruction opcode manual and started isolating all the instructions that have ASCII printable opcodes, and then filtered them even further to obtain a good set of instructions that can manipulate data on the stack and do some operations on it.

I ended with this encoder, and it worked really fine. But the problem is that it produces a very large output that in some cases cannot fit into the stack. But this project was intended only for the sake of the concept and nothing else, but now I am thinking to do some improvements on it. Like making multiple nested encoders/decoders, and handcrafting them more efficiently.

The project is written in python and is entirely contained in the ShellCodeEncoder.py file.
