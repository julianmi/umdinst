/**
 * A program that outputs its first command-line argument to standard out,
 * its second command-line argument to standard error, and its third it uses
 * is either 0 for success or -1 for failure
 */

#include <stdio.h>
#include <stdlib.h>
#include "outerr.h"


int main(int argc, char *argv[])
{
	const char *outstring, *errstring;
	int res = 0;
	
	if(argc>=2) {
		outstring = argv[1];
		fprintf(stdout,outstring);
		if(argc>=3) {
			errstring = argv[2];
			fprintf(stderr,errstring);
			if(argc>=4) {
				res = atoi(argv[3]);
			}
		}
	}
	if(res==0) {
		return EXIT_SUCCESS;
	} else {
		return EXIT_FAILURE;
	}
}
