#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
//#include <image.h>

#define FL_HI 16
#define FL_LO 17
#define CS_HI 28
#define CS_LO 29

static void usage();
static int do_chksum( char *ifile, char *ofile);

static void usage(char *name)
{
	fprintf(stderr, "usage: %s ifile ofile\n", name);
	exit(-1);
}

static int do_chksum(char *ifile, char *ofile)
{
	FILE *ifp=0;
	FILE *ofp=0;
	int rc = -1;
	struct stat st;
	unsigned char *buf=0;
	unsigned int data;
	unsigned int chksum;
	int i;
	int len;

	if (rc=stat(ifile, &st))
	{
		fprintf(stderr, "stat err =%d, %s\n", rc, strerror(rc));
		goto err;	
	}

	if (st.st_size==0)
	{
		fprintf(stderr, "file (%s) size=0\n", ifile);
		goto err;
	}

	if ((ifp = fopen(ifile, "r")) == NULL )
	{
		fprintf(stderr, "ERR: fopen(%s)\n", ifile);
		goto err;
	}

	if ((ofp = fopen(ofile, "w")) == NULL )
	{
		fprintf(stderr, "ERR: fopen(%s)\n", ofile);
		goto err;
	}

	len=(int)st.st_size;
	//fprintf(stderr, "file size=%d (0x%x)\n",len, len);

	if ((buf=(char*) malloc( len+1024 ))==0)
	{
		fprintf(stderr, "ERR: malloc\n");
		goto err;
	}
	memset(buf, 0, len+256);

	if ( (rc=fread(buf, len, 1,  ifp)) != 1 )
	{
		fprintf(stderr, "ERR: fread(%s) rc=%d\n",ifile, rc);
		rc = -1;
		goto err;
	}
	else
		rc =0;
	len=(len+3)&~3; //align to 4 bytes

	buf[FL_LO] |= (1<<2); /* IH_CHKSUM_EN */ 
	chksum=0;
	for (i=0; i<len; i+=2)
	{
		data = (buf[i]<<8) | buf[i+1];
		chksum += data;
		while (chksum>>16)
			chksum = (chksum&0xffff) + (chksum>>16);
		//printf("%04x\n", chksum);
	}
	printf("org=0x%04x ", chksum);
	chksum = (0xffff ^ chksum)  ;
	printf("chksum=0x%04x\n", chksum);
	//chksum++;
	buf[CS_HI]=(chksum>>8)&0xff;
	buf[CS_LO]=(chksum)&0xff;

	rc = 0;

	if ( (rc=fwrite(buf, len, 1, ofp)) != 1 )
	{
		fprintf(stderr, "ERR: fwrite(%s) rc=%d\n", ofile, rc);
		goto err;
	}

err:
	if (buf)
		free(buf);

	if (ifp)
		fclose(ifp);

	if (ofp)
		fclose(ofp);

	return rc;
}

int main(int argc, char* argv[])
{
	if (argc != 3) 
	{
		usage(argv[0]);
	}

	if (do_chksum(argv[1], argv[2]) < 0) 
	{
		return -1;
	}
	return 0;
}
