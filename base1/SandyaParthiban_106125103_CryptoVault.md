Crypto base task, stage1:

The top 3 plaintexts for the given message:

1.The quick brown fox jumps over the lazy dog. Cryptography is the art of writing and solving codes.

2.Nby kocwe vliqh zir dogjm ipyl nby futs xia. Wlsjnialujbs cm nby uln iz qlcncha uhx mifpcha wixym.

3.Jxu gkysa rhemd ven zkcfi eluh jxu bqpo tew. Shofjewhqfxo yi jxu qhj ev mhyjydw qdt ieblydw setui.
___________________________________________________________________________________________________________________________
STAGE_1:

Here the concept of Caesar Cipher, a common substitution encryption method, where the alphabets in the plaintext are shifted by a fixed number of positions and replacing the original letters.Decryption is done by reversing the shift.

It ensures confidentiality as the original text is obscured from casual observation, which makes understanding the text harder without the shift.

It's drawback is that there are only 25 shifts (keys) possible and hence can be easily broken by brute-forcing or frequency analysis as certain letters tend to appear more often than others in a language. 

QUESTIONS:

1.Why is Caesar trivially breakable?

  Caesar is trivially breakable as there are only 25 possible keys for a cipher,which can be easily breaked using brute-fforcing or techniques like frequency analysis.

2. What property of language makes frequency analysis work?
 
  Certain letters of the alaphabet being used in greater frequency than others make the technique work.For example the letter "e" is the most used letter in English.So by shifting these repeated letters correctly the cipher can be cracked.
_______________________________________________________________________________________________________________________
STAGE_2:

The concept used here is hash function (Crytographic SHA-256 hash) which adds integrity to the encrypted file.Before encryption a hash is generated for the plaintext and stored alongside the cipher text. While decryption, a hash is calculated for the decrypted plaintext which is compared with the stored hash. If the stored hash and calculated hash are same, it is known that the integrity is verified, else the file is tampered with as even slightly different texts generate different hashes.

QUESTIONS(stage2):

1. Encryption gives confidentiality. Hashing gives integrity. Why do you need both?
   
   Encryption gives confidentiality by hiding the text from casual view while hashing adds integrity by making sure that it will be known if the file is tampered with.Both are required as encryption can't tell if the file is tampered while hash alone can't hide the text.

