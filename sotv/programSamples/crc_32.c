//----- Include files ---------------------------------------------------------
#include <stdlib.h>                 // Needed for rand()

//----- Type defines ----------------------------------------------------------
typedef unsigned char      byte;    // Byte is a char
typedef unsigned short int word16;  // 16-bit word is a short int
typedef unsigned int       word32;  // 32-bit word is an int

//----- Defines ---------------------------------------------------------------
#define POLYNOMIAL 0x04c11db7L      // Standard CRC-32 ppolynomial
#define BUFFERLEN       4096L      // Length of buffer

//----- Gloabl variables ------------------------------------------------------
static word32 crctable[256];       // Table of 8-bit remainders

//----- Prototypes ------------------------------------------------------------
void gencrctable(void);
word32 updatecrc(word32 crcaccum, byte *datablkptr, word32 datablksize);

//===== Main program ==========================================================
void main(void)
{
  byte        buff[BUFFERLEN]; // Buffer of packet bytes
  word32      crc32;            // 32-bit CRC value
  word16      i;                // Loop counter (16 bit)
  word32      j;                // Loop counter (32 bit)

  // Initialize the CRC table
  gencrctable();

  // Load buffer with BUFFERLEN random bytes
  for (i=0; i<BUFFERLEN; i++)
    buff[i] = (byte) rand();

  // Compute and output CRC
  crc32 = updatecrc(-1, buff, BUFFERLEN);
}

//=============================================================================
//=  CRC32 table initialization                                               =
//=============================================================================
void gencrctable(void)
{
  register word16 i, j;
  register word32 crcaccum;

  for (i=0;  i<256;  i++)
  {
    crcaccum = ( (word32) i << 24 );
    for ( j = 0;  j < 8;  j++ )
    {
      if ( crcaccum & 0x80000000L )
        crcaccum = (crcaccum << 1) ^ POLYNOMIAL;
      else
        crcaccum = (crcaccum << 1);
    }
    crctable[i] = crcaccum;
  }
}

//=============================================================================
//=  CRC32 generation                                                         =
//=============================================================================
word32 updatecrc(word32 crcaccum, byte *datablkptr, word32 datablksize)
{
   register word32 i, j;

   for (j=0; j<datablksize; j++)
   {
     i = ((int) (crcaccum >> 24) ^ *datablkptr++) & 0xFF;
     crcaccum = (crcaccum << 8) ^ crctable[i];
   }
   crcaccum = ~crcaccum;

   return crcaccum;
}