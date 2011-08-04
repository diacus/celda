#include <stdio.h>
#include <stdlib.h>
#include <string.h>

unsigned int orden;
unsigned int expo[256];
unsigned int loga[256];
unsigned int a[5][3] = {
	'1', '3', '2' ,
	'1', '1', '1' ,
	'2', '3', '1' ,
	'2', '2', '3' ,
	'2', '3', '3'
};

unsigned int b[3];
const int    PRIMITIVO = 369;

//@ recorre 'v' a la derecha y determina la ultima vez que el LSb es 1 o 0.
//  -----------------------------------------------------------------------
int grado(int v) {
   	int i, j;
	unsigned int l, w;

	l = 0;
	w = 1;
	j = 8*sizeof(i);
	for (i=1; i<j; i++)
	{  l=(v&w)? i: l;
		v=(v>>1);   
	};
	return l;
}

//@ suma en modulo 2 bit por bit
//  -----------------------------------------------------------------------
unsigned int suma(unsigned int a, unsigned int b) { return(a^b); }

//@ multiplicacion por medio de logaaritmos
//  -----------------------------------------------------------------------
unsigned int mult(unsigned int a, unsigned int b)
{
	//   cout << " mult " << a << "x" << b;
	if ((a!=0)&&(b!=0))
		return(expo[(loga[a]+loga[b])%orden]);
	else
		return(0);
}

//@ genera el campo finito a partir de su polinomio primitivo.
//  -----------------------------------------------------------------------
void generaGF() {
   	unsigned int      dg;        // cociente parcial ("toca a 0 o 1?")
	unsigned int      rx;        // residuo
	unsigned int      gx;        // polinomio primitivo
	unsigned int     ngx;        // g(x), desplazamiento a la izq.

	int leng1        = 0;        // grado de g(x)
	int leng2        = 0;        // grado de r(x)
	int                i;

	gx=PRIMITIVO;
	leng1 = grado(gx);
	orden = 1<<(leng1-1);
	orden = orden-1;

	rx    = 1;
	for (i=0; i<orden; i++)
	{  leng2 = grado(rx);
		dg    = 1;

		dg = (leng2-leng1>=0)?     dg<<(leng2-1): 0;
		ngx= (leng2-leng1>=0)? gx<<(leng2-leng1): 0;

		while (ngx >= gx)
		{  if (dg==(rx&dg))       // si "toca" a 1
			rx=rx^ngx;
			dg=(dg>>1);
			ngx=(ngx>>1);
		};

		expo[i]=rx;  
		loga[rx]=i;  // cout << "loga (" << rx << ")=  " << i << "\n";
		rx=rx<<1;
	};
}

int namecopies( char ***dest, char *fname ) 
{
	char **names, prefix[10];
	int i, namelen;

	namelen = strlen(fname) + 10;
	names = (char **) calloc(5, sizeof(char *));

	for( i = 0; i < 5; i++ )
	{
		sprintf( prefix, "-%d.ida", i);
		*(names + i) = (char *) calloc(namelen, sizeof(char));
		strcat( *(names + i), fname );
		strcat( *(names + i), prefix );
	}

	*dest = names;

	return 0;

}

//@ produce los cinco archivos de dispersion
//------------------------------------------------------------------
void dispersa(char *file) {
	FILE *in, *out0, *out1, *out2, *out3, *out4;
	char c1, c2, **names, **name;
	int i, j, t, size;

	namecopies( &names, file );
	name = names;

	if ((in=fopen(file, "rb"))==NULL)
	{  printf("no puedo abrir el archivo fuente\n");
		exit(1);
	}

	if ((out0=fopen(*name++, "wb"))==NULL)
	{  printf("no puedo crear un disperso\n");
		exit(1);
	}

	if ((out1=fopen(*name++, "wb"))==NULL)
	{  printf("no puedo crear un disperso\n");
		exit(1);
	}

	if ((out2=fopen(*name++, "wb"))==NULL)
	{  printf("no puedo crear un disperso\n");
		exit(1);
	}

	if ((out3=fopen(*name++, "wb"))==NULL)
	{  printf("no puedo crear un disperso\n");
		exit(1);
	}

	if ((out4=fopen(*name++, "wb"))==NULL)
	{  printf("no puedo crear un disperso\n");
		exit(1);
	}

	// Los n+1 primeros bytes del archivo son: |F|mod(n), el exceso del archivo
	// fuente y los n bytes del renglon de la matriz que da origen al disperso

	for (i=0; i<5; i++)
		switch (i)
		{  case 0:  putc(' ', out0);  
			for (j=0; j<3; j++) putc(a[i][j], out0);
			break;
			case 1:  putc(' ', out1);  
					 for (j=0; j<3; j++) putc(a[i][j], out1);
					 break;
			case 2:  putc(' ', out2);  
					 for (j=0; j<3; j++) putc(a[i][j], out2);
					 break;
			case 3:  putc(' ', out3);  
					 for (j=0; j<3; j++) putc(a[i][j], out3);
					 break;
			case 4:  putc(' ', out4);  
					 for (j=0; j<3; j++) putc(a[i][j], out4);
					 break;
		};


	size=0;
	while (!feof(in))
	{
		for (j=0; j<3; j++)
			b[j]=0;

		j=0;
		do
		{  b[j++]=getc(in);

			if (!feof(in)) 
				size++;
		}
		while ((!feof(in))&&(j<3));

		if (j>0)
			for (i=0; i<5; i++)
			{  t=0;
				for (j=0; j<3; j++)
					t=suma(t, mult(a[i][j],b[j]));
				c2=t;
				switch (i)
				{  case 0:  putc(t, out0);  
					break;
					case 1:  putc(t, out1);  
							 break;
					case 2:  putc(t, out2);  
							 break;
					case 3:  putc(t, out3);  
							 break;
					case 4:  putc(t, out4);  
							 break;
				};

			};

	};

	fclose(in);

	rewind(out0);    putc(size%3, out0);   fclose(out0);
	rewind(out1);    putc(size%3, out1);   fclose(out1);
	rewind(out2);    putc(size%3, out2);   fclose(out2);
	rewind(out3);    putc(size%3, out3);   fclose(out3);
	rewind(out4);    putc(size%3, out4);   fclose(out4);
}


//@ 
//------------------------------------------------------------------
main(int argc, char **argv)
{

	if (argc!=2)
	{  printf("olvido ingresar el nombre del archivo fuente\n");
		exit(1);
	}


	generaGF();
	dispersa(argv[1]);
}
