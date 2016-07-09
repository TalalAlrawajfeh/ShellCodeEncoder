#Python 2

import os

strFile = raw_input("Insert the binary opcodes file path: ")

if not os.path.isfile(strFile):
	print "The path you inserted doesn't exist."
	exit()

def FindXorPair(Asc):
	X = 0x30
	while X <= 0x7A:
		Y = 0x30
		while Y <= 0x7A:
			if X ^ Y == Asc:
				return (X, Y)
			
			Y += 1
			if Y > 0x39 and Y < 0x41:
				Y = 0x41
			if Y > 0x5A and Y < 0x61:
				Y = 0x61
		X += 1
		if X > 0x39 and X < 0x41:
			X = 0x41
		if X > 0x5A and X < 0x61:
			X = 0x61

def CreateTempFile(strPath, strExtension):
	i = len(strPath) - 1
	while i >= 0:
		char = strPath[i]
		if char == '\\' or char == '.':
			break
		i -= 1

	if char == '\\':
		strFileName = strPath
	if char == '.':
		strFileName = strPath[0:i]
	
	strTempFile = strFileName + "." + strExtension
	if not os.path.isfile(strTempFile):
		return strTempFile

	i = 1
	while True:
		strTempFile = strFileName + " (" + str(i) + ")." + strExtension
		if not os.path.isfile(strTempFile):
			return strTempFile
		i += 1

def IsAlphaNumeric(Asc):
	if Asc >= 0x30 and Asc <= 0x39:
		return True
	if Asc >= 0x41 and Asc <= 0x5A:
		return True
	if Asc >= 0x61 and Asc <= 0x7A:
		return True
	return False

strDecoder = ""
strEncoded = ""

File = open(strFile, "rb")
strRead = File.read(4)

while strRead != "":
	if len(strRead) < 4:
		strRead += '0' * (4 - len(strRead))
	
	i = 0
	IsSmall = True
	while i < 4:
		if ord(strRead[i]) >= 0x80:
			IsSmall = False
			break
		i += 1

	if IsSmall:
		i = 0
		n = 0
		AlphaNum = True
		while i < 4:
			if not IsAlphaNumeric(ord(strRead[i])):
				AlphaNum = False
				n += 1
			i += 1
		
		if AlphaNum:
			strDecoder += 'X' #POP  EAX
			strEncoded += strRead
		else:
			asc = ord(strRead[0])
			if not IsAlphaNumeric(asc) and n == 1:
				XorCode = FindXorPair(asc)
				
				strDecoder += 'X' #POP  EAX
				strDecoder += '4' + chr(XorCode[1]) #XOR  AL, BYTE
				strDecoder += 'P' #PUSH EAX
				strDecoder += 'X' #POP  EAX
				strEncoded += chr(XorCode[0]) + strRead[1:4]
			else:
				i = 0
				Xor = ""
				while i < 4:
					asc = ord(strRead[i])
					XorCode = FindXorPair(asc)
					strEncoded += chr(XorCode[0])
					Xor += chr(XorCode[1])
					i += 1
				
				strDecoder += 'X' #POP  EAX
				strDecoder += '5' + Xor #XOR  EAX, DWORD
				strDecoder += 'P' #PUSH EAX
				strDecoder += 'X' #POP  EAX
	else:
		i = 0
		n = 0
		Xor1 = ""
		Xor2 = ""
		while i < 4:
			asc = ord(strRead[i])
			if asc < 0x80:
				XorCode = FindXorPair(asc)
				strEncoded += chr(XorCode[0])
				XorCode = FindXorPair(XorCode[1])
				Xor1 += chr(XorCode[0])
				Xor2 += chr(XorCode[1])
			else:
				strEncoded += 'z' #0x7A
				XorCode = FindXorPair(asc ^ 0x80)
				Xor1 += chr(XorCode[0])
				Xor2 += chr(XorCode[1])
				n += 1
			i += 1

		i = 0
		while i < 4:
			if ord(strRead[i]) >= 0x80:
				strDecoder += 'Y' #POP  ECX
				strDecoder += 'A' * 6 #INC  ECX (6 TIMES)
				strDecoder += 'Q' #PUSH ECX

				n -= 1
				if n == 0:
					break
			
			strDecoder += 'D' #INC  ESP
			i += 1

		if i > 0:
			strDecoder += 'L' * i #DEC  ESP
			
		strDecoder += 'X' #POP  EAX
		strDecoder += '5' + Xor1 #XOR  EAX, DWORD
		strDecoder += '5' + Xor2 #XOR  EAX, DWORD
		strDecoder += 'P' #PUSH EAX
		strDecoder += 'X' #POP  EAX

	strRead = File.read(4)
File.close()

i = len(strDecoder) / 31
j = (len(strDecoder) % 31) / 3
k = (len(strDecoder) % 31) % 3

strEsp = 'a' * i #POPAD (i TIMES)
strEsp += 'X' * (j + k) #POP  EAX (i + k TIMES)
strEsp += 'L' * k  #DEC  ESP (k TIMES)

strCodeFile = CreateTempFile(strFile, "code")
File = open(strCodeFile, "wb")
File.write(strEsp)
File.write(strDecoder)
File.write(strEncoded)
File.close()
