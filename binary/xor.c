#include <stdio.h>
#include <string.h>

#define MAX_SIZE 1000  // max length for the strings

void xor_strings(char *s1, const char *s2, char *resultHex) {
    size_t len1 = strlen(s1);
    size_t len2 = strlen(s2);
    size_t i;

    for (i = 0; i < len1; i++) {
        s1[i] ^= s2[i % len2];
        // hex representation
        sprintf(&resultHex[i*2], "%02x", (unsigned char)s1[i]); 
    }
}

int main() {
    char str1[MAX_SIZE], str2[MAX_SIZE], resultHex[MAX_SIZE * 2];

    printf("Enter the first string (up to %i characters): ", MAX_SIZE);
    fgets(str1, MAX_SIZE, stdin); 
    // Remove newline 
    str1[strcspn(str1, "\n")] = 0; 

    printf("Enter the second string (up to %i characters): ", MAX_SIZE);
    fgets(str2, MAX_SIZE, stdin);
    str2[strcspn(str2, "\n")] = 0;

    xor_strings(str1, str2, resultHex);

    printf("XORed String: %s\n", str1);
    printf("As hex: %s\n", resultHex);

    return 0;
}