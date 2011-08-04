#include <stdio.h>
#include <stdlib.h>

unsigned int orden;
unsigned int expo[255];
unsigned int loga[255];
unsigned int a[3][3];
unsigned int g[3][3];
unsigned int d[3];
const    int PRIMITIVO = 369;


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

//@ division por medio de logaaritmos
//  -----------------------------------------------------------------------
	unsigned int division(unsigned int a, unsigned int b)
{  if (b==0)
	return(orden+1);
	else
		if (a==0)
			return(0);
		else
			return(expo[(loga[a]+orden-loga[b])%orden]);
}


//@ invierte una matriz cuadrada de 3x3
//  -----------------------------------------------------------------------
void invierteM()
{
	int i,j;
	unsigned int d;

	d=0;
	for (j=0; j<3; j++)
		d=suma(d,mult(a[0][j],
					suma(mult(a[1][(j+1)%3],a[2][(j+2)%3]),
						mult(a[1][(j+2)%3],a[2][(j+1)%3]))));

	//   cout << "d = " << d << endl;

	for (i=0; i<3; i++)
		for (j=0; j<3; j++)
			g[j][i]=division(suma(mult(a[(i+1)%3][(j+1)%3],a[(i+2)%3][(j+2)%3]),
						mult(a[(i+1)%3][(j+2)%3],a[(i+2)%3][(j+1)%3])),
					d);
}


//@ genera el campo finito a partir de su polinomio primitivo.
//  -----------------------------------------------------------------------
void generaGF()
{  unsigned int      dg;        // cociente parcial ("toca a 0 o 1?")
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
		//      cout << "expo[" <<i << "]=" << rx<< ",\n";
		loga[rx]=i;
		rx=rx<<1;
	};
}

//@ reconstruye el archivo original a partir de sus pedazos
//------------------------------------------------------------------
void recupera(char *file0, char *file1, char *file2, char *file3)
{
	FILE *in0, *in1, *in2, *out;
	char c, b[3], c3[12]={0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
	int i, j, r, primera;
	unsigned int t, *aux[3];

	if ((in0=fopen(file0, "rb"))==NULL)
	{  printf("no puedo abrir disperso\n");
		exit(1);
	}

	if ((in1=fopen(file1, "rb"))==NULL)
	{  printf("no puedo abrir disperso\n");
		exit(1);
	}

	if ((in2=fopen(file2, "rb"))==NULL)
	{  printf("no puedo abrir disperso\n");
		exit(1);
	}

	if ((out=fopen(file3, "wb"))==NULL)
	{  printf("no puedo abrir archivo destino\n");
		exit(1);
	}

	for (i=0; i<3; i++)
		switch (i)
		{
			case 0:
				r=getc(in0);  
				for (j=0; j<3; j++) a[i][j]=getc(in0);
				break;
			case 1: 
				r=getc(in1);  
				for (j=0; j<3; j++) a[i][j]=getc(in1);
				break;
			case 2: 
				r=getc(in2);  
				for (j=0; j<3; j++) a[i][j]=getc(in2);
				break;
		};

	invierteM();
	primera=1;
	for (j=0; j<3; j++)
		aux[j] = (unsigned int *) &c3[4*j];

	do {
	   	for (j=0; j<3; j++)
		switch (j)
		{  case 0:  c=getc(in0);
			if (!feof(in0)) 
			{  c3[4*j]=c;
				d[j]=(*aux[j]);
			}
			break;
			case 1:  c=getc(in1);
					 if (!feof(in1))
					 {  c3[4*j]=c;
						 d[j]=(*aux[j]);
					 };
					 break;
			case 2:  c=getc(in2);
					 if (!feof(in2))
					 {  c3[4*j]=c;
						 d[j]=(*aux[j]);
					 };
					 break;
		};

		if ((!feof(in0))&&(!primera))
		{  for (i=r; i<3; i++)
			putc(b[i], out);
		}

		if (!feof(in0)) { 
			for (i=0; i<3; i++) {
		   	t=0;
				for (j=0; j<3; j++)
					t=suma(t, mult(g[i][j], d[j]));
				b[i]=t;
			}

			for (i=0; i<r; i++)
				putc(b[i], out);
		}

		if (feof(in0)&&(r==0))	
			for (i=r; i<3; i++)
				putc(b[i], out);

		primera=0;
	}
	while (!feof(in0));

	fclose(in0);
	fclose(in1);
	fclose(in2);
	fclose(out);
}


//@ 
//------------------------------------------------------------------
main(int argc, char **argv)
{
	if (argc!=5) {
	   	printf("olvido ingresar el nombre de un archivo\n");
		exit(1);
	}

	generaGF();
	recupera(argv[1], argv[2], argv[3], argv[4]);
}
