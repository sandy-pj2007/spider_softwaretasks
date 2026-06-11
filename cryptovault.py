import sys
import hashlib
def get_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()
def encrypt(text,shift):
    shift=shift%26
    en_str=""
    for j in text:
        i=ord(j)
    
        if (i>=97 and i<=122):
            i+=shift
            if (i>122):
                i-=26
        elif (i>=65 and i<=90):
            i+=shift
            if (i>90):
                i-=26
        en_str+=chr(i)
    return en_str    

def decrypt(text,shift):
    shift%=26
    en_str=""
    for j in text:
        i=ord(j)
    
        if (i>=97 and i<=122):
            i-=shift
            if (i<97):
                i+=26
        elif (i>=65 and i<=90):
            i-=shift
            if (i<65):
                i+=26
        en_str+=chr(i)
    return en_str
 
def crack(text):
    list=[]
    common="ETAOINSHetaoinsh"
    results=[]
    for k in range(1,26):
        list.append(decrypt(text,k))
    for i in list:
        score=0
        for j in i:
            if j in common:
                score+=1
        results.append((score,i))
    results.sort(reverse=True)
    for x,y in results[:3]:
        print(y)


        
                
mode=sys.argv[1]
filename=sys.argv[2]
verify="--verify" in sys.argv
if mode=="crack":
    with open(filename,"r") as f:
        lines=f.readlines()
        text=lines[1:]
    crack(text)
else:
    shift=int(sys.argv[4])
    if mode=="encrypt":
        with open(filename,"r") as f:
          text=f.read()
        hash_value=get_hash(text)
        ciphertext=encrypt(text,shift)
        with open(filename+".enc","w") as f:
          f.write(hash_value+"\n")
          f.write(ciphertext)
          print("Encryption complete")
    elif mode=="decrypt":
        with open(filename,"r") as f:
            lines=f.readlines()
        stored_hash=lines[0].strip()
        ciphertxt="".join(lines[1:])
        plaintxt=decrypt(ciphertxt,shift)
        print(plaintxt) 
        if verify:
            current_hash=get_hash(plaintxt)
            if current_hash==stored_hash:
                print("Integrity is verified")
            else:
                print("Hashes don't match, file has been tampered.")   
        
    else:
        print("invalid mode")