
void dns_build_19(unsigned char *b) {
    b[0] = 0x13; b[1] = 0xAA; // ID
    b[2] = 0x01; b[3] = 0x00; // Standard Query
    for(int i=4; i<12; i++) b[i] = 0; 
}